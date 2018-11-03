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
    ser.port = '/dev/cu.usbmodem145401'   #COM Port Name Start from 0
    #ser.port = '/dev/ttyUSB0' #If Using Linux
 
    #Specify the TimeOut in seconds, so that SerialPort
    #Doesn't hangs
    ser.timeout = 1
    ser.open()          #Opens SerialPort

    # print port open or closed
   
# #Function Ends Here

init_serial()
   
vol = OSAX()
 
while True:
    incoming = ser.readline()
    
    #print (int(incoming.decode('utf-8'))) # print the current volume
    volume = float(int(incoming.decode('utf-8'))/103*7)      
    vol.set_volume(volume) #system volume control





# buttonStateFlag = True
# playStateFlag = False

# while True:
#     data = ser.readline()
#     #Self-locking Push Switch for Play/Pause 
#     if data == 400 and buttonStateFlag == True: 
#         playStateFlag = not playStateFlag
#         if playStateFlag:
#             print("Play") #need api calling
#         else:
#             print("Pause") #need api calling
#         buttonStateFlag = False
    
#     elif data < 400:
#         buttonStateFlag = True
#         #volume control
#         if data < 105:
#             volume = data
#             #print("Volume: %d" %volume)

#         #play previous
#         elif data == 200:
#             print("Play Previous") #need api calling
#         #play next
#         elif data == 300:
#             print("Play Next") #need api calling
#     applescript.Applescript("set volume output volume %d" % volume).run() #System volume control on Mac