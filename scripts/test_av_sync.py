import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import cv2

sound = sf.read('recordings/sounds/test.wav')
sound_time_start = np.loadtxt('recordings/sounds/test.txt')
print(sound)
print(sound_time_start)
#plt.plot(sound[0])
#plt.show()

peak = np.argmax(sound[0])
time_clap = sound_time_start + peak/sound[1]
print(peak)
print(time_clap)


video = cv2.VideoCapture('recordings/videos/test.avi')
video_times = np.loadtxt('recordings/videos/test.txt')

print(video_times - time_clap)
video_frame_clap = np.argmax(video_times - time_clap > 0)
print(video_frame_clap)
print(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))

video.set(1, video_frame_clap)
res, frame = video.read()
cv2.imshow('test', frame)

while True:
    ch = 0xFF & cv2.waitKey(1) # Wait for a second
    if ch == 27:
        break