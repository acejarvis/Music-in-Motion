#Jarvis Wang
#test on Mac using port /dev/cu.usbmoderm145401
import applescript
import serial
import math
buttonStateFlag = True
playStateFlag = False
#read data from arduino
ser = serial.Serial("/dev/cu.usbmoderm145401", 9600, timeout = 0.5)
while True:
    data = ser.readline()
    #Self-locking Push Switch for Play/Pause
    if data == 400 and buttonStateFlag == True: 
        playStateFlag = not playStateFlag
        if playStateFlag:
            print("Play") #need api calling
        else:
            print("Pause") #need api calling
        buttonStateFlag = False
    
    elif data < 400:
        buttonStateFlag = True
        #volume control
        if data < 105:
            volume = data
            #print("Volume: %d" %volume)

        #play previous
        elif data == 200:
            print("Play Previous") #need api calling
        #play next
        elif data == 300:
            print("Play Next") #need api calling
    applescript.Applescript("set volume output volume %d" % volume).run()