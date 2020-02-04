#!/usr/bin/env python3
"""Plot and store the live microphone signal.


"""
import argparse
import queue
import sys
import time
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import numpy as np
assert np

from matplotlib.animation import FuncAnimation

# Optional arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-n', '--name', type = str, default = '')
parser.add_argument('-sP', '--showPlot', type = bool, default = False)
parser.add_argument('-d', '--duration', type = int, default = 0)
args = parser.parse_args()

# recording parameters (same freq and resolution as original paper)
samplerate = 44100 # change to match recording speed of device, but only need 8000
device = 2
channels = [1]
subtype = 'PCM_16'
recording_dir = 'recordings/sounds/'

if args.name == '':
    filename = recording_dir + 'wingbeats_' + time.strftime('%D__%T').replace('/','_').replace(':','_') + '.wav'
else:
    filename = recording_dir + args.name + '.wav'
    
# plot parameters
downsample = 50
interval = 20
window = 200


q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    if args.showPlot:
        q.put(indata[::downsample, [c - 1 for c in channels]])
    else:
        q.put(indata.copy())

def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines

try:
    length = int(window * samplerate / (1000 * downsample))
    plotdata = np.zeros((length, len(channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)


    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate,
        channels=max(channels), subtype=subtype) as file:
        with sd.InputStream(samplerate = samplerate,
                            device = device,
                            channels = max(channels),
                            callback = audio_callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)

            if args.showPlot == True:
                while True:
                    plt.plot()
                    plt.draw()
                    plt.pause(0.001)
                    file.write(q.get())
            else:
                while True:
                    file.write(q.get())

except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(filename))
    exit(0)


