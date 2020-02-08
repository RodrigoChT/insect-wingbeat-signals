import argparse
import time

from record_testing import start_AVrecording
from record_testing import stop_AVrecording

# Script arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-d', '--duration', type = int, default = 0, required = True)
parser.add_argument('-r', '--repetitions', type = int, default = 1)
parser.add_argument('-n', '--fileName', type = str, default = 'None')
parser.add_argument('-sV', '--showVideo', type = int, default = 0)
parser.add_argument('-aD', '--audioDirectory', type = str, default = 'recordings/sounds/')
parser.add_argument('-vD', '--videoDirectory', type = str, default = 'recordings/videos/')
args = parser.parse_args()

if args.fileName is not None:
    name_addon = args.fileName + '_'
else:
    name_addon = ''

for i in range(args.repetitions):

    current_file_name =  name_addon + \
                         time.strftime('%D__%T').replace('/','_').replace(':','_')


    start_AVrecording(file_name = current_file_name,
                      video_device_index = -1, # 0 for laptop
                      audio_device_index = 0, # 16 for laptop
                      show_video = args.showVideo,
                      audio_directory = args.audioDirectory,
                      video_directory = args.videoDirectory,
                      rate = 44100) # 8000 for laptop

    time.sleep(args.duration)

    stop_AVrecording(current_file_name)

    time.sleep(2)


