
# coding: utf-8

# In[38]:


import pyaudio
import struct              
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'tk')

CHUNK = 1024*4                            # (arbitrary) num-frames audio signals are split-into
FORMAT = pyaudio.paInt16                  # 16-bit sample-size
CHANNELS = 1                              # 1 audio-source
RATE = 44100                              # (Hz) sampling-rate 


# In[ ]:


# PortAudio Object
p = pyaudio.PyAudio()  

# Open Microphone | Read Audio 
stream = p.open(
    format = FORMAT, channels = CHANNELS, rate = RATE,        # not sure how ^ opens mic
    input=True, output=True, frames_per_buffer = CHUNK
)

# Init Plot
fig, ax = plt.subplots()
x = np.arange(0, 2*CHUNK, 2)                     # domain = 0 : 2 : 2*CHUNK
line, = ax.plot(x, np.random.rand(CHUNK))        # initial plot = arbitary 

ax.set_ylim(0,255)
ax.set_xlim(0,CHUNK)

# Plot Audio Data
while True:
    dataBin = stream.read(CHUNK) 
    dataInt = np.array(struct.unpack(str(2*CHUNK) + 'B', dataBin), dtype = 'b')[::2] + 128     #constrain in 0-255
    line.set_ydata(dataInt)
    fig.canvas.draw()
    fig.canvas.flush_events()


# In[12]:





