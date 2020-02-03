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

# recording parameters (same freq and resolution as original paper)
samplerate = 8000
device = 9
channels = [1]
subtype = 'PCM_16'
filename = 'recordings/wingbeats_' + time.strftime('%D__%T').replace('/','_').replace(':','_') + '.wav'

# plot parameters
downsample = 10
interval = 20
window = 200

q = queue.Queue()

# Do not show plot by default
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-sP', '--showPlot', type = bool, default = False)
parser.add_argument('-d', '--duration', type = int, default = 0)
args = parser.parse_args()

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
        with sd.InputStream(samplerate=samplerate,
                            channels=max(channels), callback=audio_callback):
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


