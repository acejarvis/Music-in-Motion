#Jarvis Wang
#test on Mac using port /dev/cu.usbmodem145401
from osax import *
import serial
import time
#import pyautogui


#read data from arduino
# ser = serial.Serial("/dev/cu.usbmodem145301", 9600) #serial ports setting on Mac
#ser = serial.Serial("COM3", 9600, timeout = 0.5) #serial ports setting on Windows

ser = 0

#Function to Initialize the Serial Port
def init_serial():
    global ser          #Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/cu.usbserial-14540'   #COM Port Name Start from 0
    #ser.port = '/dev/ttyUSB0' #If Using Linux
 
    #Specify the TimeOut in seconds, so that SerialPort
    #Doesn't hangs
    ser.timeout = 1
    ser.open()          
    
    #Opens SerialPort

    # print port open or closed
   
# #Function Ends Here

init_serial()
   
vol = OSAX()

# buttonStateFlag = True
# playStateFlag = True 
# counter_sum = 0
# counter_left = 0
# counter_right = 0

while True:

    incoming = ser.readline()
    data = int(incoming.decode('utf-8'))
    print(data)
    #Self-locking Push Switch for Play/Pause 
#convert to int
    volume = float(data/103*7)      
    vol.set_volume(volume) #system volume control


#     if data < 120:
#         volume = float(data/103*7)      
#         vol.set_volume(data) #system volume control

#     if data ==202:
#         counter_sum +=1
#     elif data == 203:
#         counter_left +=1
#     elif data == 302:
#         counter_right +=1
#     else: 
#         counter_left = 0
#         counter_right = 0
#         counter_sum = 0
    
#     # condition
#     if counter_left >= 10 and counter_left <= 20 or counter_right >= 10 and counter_right <= 20:
#         if counter_left > counter_right:
#             print("play previous")
#         else: 
#             print("play next")

#     if counter_sum > 20:
#         buttonStateFlag = True

#     if buttonStateFlag == True: 
#         playStateFlag = not playStateFlag
#         if playStateFlag:
#             print("Play") #need api calling
#         else:
#             print("Pause") #need api calling
        
#         buttonStateFlag = False
    
    