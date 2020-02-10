import cv2
import threading
import time
import queue
import sounddevice as sd
import soundfile as sf
import sys

class VideoRecorder():

	# Video class based on openCV
	def __init__(self,
				 file_name,
				 video_device_index,
				 video_directory,
				 show_video):

		self.open = True
		self.video_device_index = video_device_index
		self.fps = 10
		self.show_video = show_video
		self.fourcc = "MJPG"
		self.frameSize = (640, 480)
		self.video_file_name = video_directory + file_name + '.avi'
		self.video_time_file_name = video_directory + file_name + '.txt'
		self.video_cap = cv2.VideoCapture(self.video_device_index)
		self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
		self.video_out = cv2.VideoWriter(self.video_file_name, self.video_writer, self.fps, self.frameSize)
		self.frame_counts = 1
		self.start_time = time.time()

	# Video starts being recorded
	def record(self):

		with open(self.video_time_file_name, 'w+') as time_data_file:
			while (self.open == True):
				ret, video_frame = self.video_cap.read()
				if (ret == True):
					self.video_out.write(video_frame)
					time_data_file.write(str(time.time()) + '\n')
					self.frame_counts += 1

					# USING THIS GENERATES THE ERROR "SEGMENTATION FAULT"
					# if self.show_video:
					# 	gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
					# 	cv2.imshow('video_frame', gray)
					# 	cv2.waitKey(1)
				else:
					break

	# Finishes the video recording therefore the thread too
	def stop(self):

		if self.open == True:

			self.open = False
			self.video_out.release()
			self.video_cap.release()
			cv2.destroyAllWindows()

		else:
			pass

	# Launches the video recording function using a thread
	def start(self):
		self.record()
		#video_thread.start()


class AudioRecorder():
	def __init__(self,
				 file_name,
				 samplerate,
				 audio_device_index,
				 audio_directory):
		self.open = True
		self.audio_file_name = audio_directory + file_name + '.wav'
		self.audio_time_file_name = audio_directory + file_name + '.txt'
		self.samplerate = samplerate
		self.q = queue.Queue()
		self.audio_device_index = audio_device_index

	def audio_callback(self, indata, frames, time, status):
		"""This is called (from a separate thread) for each audio block."""
		if status:
			print(status, file=sys.stderr)
		self.q.put(indata.copy())
		#self.q.put(indata[::downsample, mapping])

	def record(self):
		# Make sure the file is opened before recording anything:
		with open(self.audio_time_file_name, 'w+') as time_data_file:
			time_data_file.write(str(time.time()))
		with sf.SoundFile(self.audio_file_name,
						  mode='x',
						  samplerate=self.samplerate,
						  channels=1,
						  subtype='PCM_16') as file:

			with sd.InputStream(samplerate=self.samplerate,
								device=self.audio_device_index,
								channels=1,
								callback=self.audio_callback):
				while self.open:
					file.write(self.q.get())
					if self.open == False:
						break


	# Finishes the audio recording therefore the thread too
	def stop(self):
		if self.open == True:
			self.open = False
		pass


	# Launches the audio recording function using a thread
	def start(self):
		audio_thread = threading.Thread(target=self.record)
		audio_thread.start()


def start_AVrecording(file_name,
					  video_device_index,
					  audio_device_index,
					  show_video = False,
					  audio_directory = 'recordings/sounds/',
					  video_directory = 'recordings/videos/',
					  rate = 44100):
	global video_thread
	global audio_thread

	video_thread = VideoRecorder(file_name,
								 video_device_index,
								 video_directory,
								 show_video)
	audio_thread = AudioRecorder(file_name,
								 rate,
								 audio_device_index,
								 audio_directory)

	audio_thread.start()
	video_thread.start()

	return file_name

def stop_AVrecording(file_name):
	audio_thread.stop()
	frame_counts = video_thread.frame_counts
	elapsed_time = time.time() - video_thread.start_time
	recorded_fps = frame_counts / elapsed_time
	print("total frames " + str(frame_counts))
	print("elapsed time " + str(elapsed_time))
	print("recorded fps " + str(recorded_fps))
	video_thread.stop()

	# Makes sure the threads have finished
	while threading.active_count() > 1:
		time.sleep(1)