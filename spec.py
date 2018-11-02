# HELLA IMPORTSSSSS
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time

plt.style.use('dark_background')

# OOP IN PYTHON , LET'S GO!

class AudioStream(object):


    def __init__(self):

        # The Mic. is used to Grab Soundwaves   

        # "Hyperparameters"
        self.CHUNK = 1024 * 2               # Soundwaves are split into 2048 "frames"
        self.FORMAT = pyaudio.paInt16       # Each "frame" has 16-bit precision
        self.CHANNELS = 1                   # Audio is obtained from 1 Channel (Mic) 
        self.RATE = 44100                   # 44,100 FPS (Hz)
        self.pause = False    

        self.p = pyaudio.PyAudio()          # 'p' is our *main* audio-object
  
        # Open Microphone per "Hyperparameters"
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        self.init_plots()
        self.start_plot()


        ''' 
        Our Program plots 2 Functions:
            (A) Raw Sound Signal                                > processed from Mic
            (B) Frequency/Volume (Spectrum Analyzer)            > Fourier-Transform of (A)
        '''

    # SET UP THE 2 PLOTS

    def init_plots(self):

        # Each Plot has a unique Domain (set of x's) 
        domainSignal = np.arange(0, 2 * self.CHUNK, 2)
        domainFft = np.linspace(0, self.RATE, self.CHUNK)

        # Our 2 Plots are Shown in Same Canvas
        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        # Initialize the 2 Plots (no data yet)
        self.lineSignal, = ax1.plot(domainSignal, np.random.rand(self.CHUNK), '-', lw=2)
        self.lineFft, = ax2.semilogx(domainFft, np.random.rand(self.CHUNK), '-', lw=2)      # "semilogx" morphs x-axis (freq.) to log-scale

        # LABELL'n
        ax1.set_title('SOUND SIGNAL')
        ax1.set_xlabel('samples'); ax1.set_ylabel('volume')
        ax1.set_ylim(0, 255); ax1.set_xlim(0, 2 * self.CHUNK)
        ax2.set_title('SPECTRUM ANALYZER')
        plt.setp(ax1, yticks=[0, 128, 255],xticks=[0, self.CHUNK, 2 * self.CHUNK])
        plt.setp(ax2, yticks=[0, 1],); ax2.set_xlim(20, self.RATE / 2)
        # show axes ??????????????????????????????????????????????????????
        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(5, 120, 1910, 1070)
        plt.show(block=False)



    # RELAY DATA TO THE 2 PLOTS

    def start_plot(self):

        # Avg.FPS = #Frames/Total-Time
        print('stream started')
        frameCount = 0; startTime = time.time()

        # Begin Reading Data
        while not self.pause:

            # Obtain a Raw Sound Signal from Mic. (Data = Binary)
            dataBin = self.stream.read(self.CHUNK)
            dataInt = struct.unpack(str(2 * self.CHUNK) + 'B', dataBin)
            dataNp = np.array(dataInt, dtype='b')[::2] + 128
            self.lineSignal.set_ydata(dataNp) # Our Plot can take Data as a Np Array

            # Perform SIGNAL PROCESSING on Raw to get Freq. Spectrum
            yf = fft(dataInt) # fft = fast fourier transform
            self.lineFft.set_ydata(np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK))

            # Draw the Obtained Data on our 2 Plots
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            frameCount += 1

        else:
            self.fr = frameCount / (time.time() - startTime) # Avg.FPS = #Frames/Total-Time
            print('average frame rate = {:.0f} FPS'.format(self.fr))
            self.exit_app()

    def exit_app(self):
        print('stream closed')
        self.p.close(self.stream)

    def onClick(self, event):
        self.pause = True


if __name__ == '__main__': # INSTANTIATE BOIS1
    AudioStream()