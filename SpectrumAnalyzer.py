# coding: utf-8

# In[25]:


import pyaudio
import struct              
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError

# to display in sep. Tk window
get_ipython().run_line_magic('matplotlib', 'tk')

CHUNK = 1024*2                            # (arbitrary) num-frames audio signals are split-into
FORMAT = pyaudio.paInt16                  # 16-bit sample-size
CHANNELS = 1                              # 1 audio-source
RATE = 44100                              # (Hz) sampling-rate 


# In[ ]:


# the plot we show the spectrum & waveform in
fig, (ax1,ax2) = plt.subplots(2, figsize=(15,7))

# PyAudio Inst. (The Audio Object)
p = pyaudio.PyAudio() 

# Open Microphone | Get Audio Waveform 
stream = p.open(
    format = FORMAT, channels = CHANNELS, rate = RATE,        # not sure how ^ opens mic
    input=True, output=True, frames_per_buffer = CHUNK
)

# We have 2 Plots: Waveform & Spectrum
xSignal = np.arange(0, 2*CHUNK, 2)                     # Waveform Domain  (0 : Num-Samples)
xFft = np.linspace(0, RATE, CHUNK)              # Spectrum Domain  (0 : Max-Freq)

# The plots' starting-frame is random 
lineSignal, = ax1.plot(xSignal, np.random.rand(CHUNK),'-',lw=2)                 # Waveform Plot
lineFft, = ax2.semilogx(xFft, np.random.rand(CHUNK),'-',lw=2)
 
# Make Graphs "Pretty"
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('Samples'); ax1.set_ylabel('Volume')
ax1.set_ylim(0, 255); ax1.set_xlim(0, 2*CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

ax2.set_xlim(20, RATE/2)

print('Our stream started!')

# FPS
frame_count = 0
start_time = time.time()

# Live Data streams to Matplotlib
while True:
    
    # The Waveform we get is in Binary | make np array
    dataBin = stream.read(CHUNK) 
    # convert data to integers, make np array, then offset it by 128
    dataInt = struct.unpack(str(2 * CHUNK) + 'B', dataBin)
    # create np array and offset by 128
    dataNp = np.array(dataInt, dtype='b')[::2] + 128  #Graph is offset by 128
    lineSignal.set_ydata(dataNp)
    
    # The Spectrum is the Fourier-Transform of our Waveform
    yf = fft(dataInt) # fft = "fast fourier transform"
    lineFft.set_ydata(np.abs(yf[0:CHUNK]) / (128*CHUNK))
    
    # update plots
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break