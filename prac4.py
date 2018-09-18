# EEE3096-prac4

#!/usr/bin/python
#--------------------------------------   
import spidev
import time
import os
import datetime
import RPi.GPIO as GPIO

#GPIO pushbutton pins setup
GPIO.setmode(GPIO.BCM)
reset = 17
frequency = 27
stop = 22
display = 23

# switchs 1,2,3,4: ifor interrupts
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequency, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(display, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#interrupt to stop recording data
def stopcallback(channel):
    global monitor
    global log_count
    
    if monitor == 1:
        monitor = 0
    elif monitor == 0:
        monitor = 1
        log_count = 0
        
#display button callback function
def displaycallback(channel):
    global monitor
    global log
    if monitor == 0:
        print("Time     Timer    pot   Temp  Light")
        print(log)

# callback functions will be called
GPIO.add_event_detect(reset, GPIO.RISING, callback=resetcallback,bouncetime=200)
GPIO.add_event_detect(frequency, GPIO.RISING, callback=freqcallback,bouncetime=200)
GPIO.add_event_detect(stop, GPIO.RISING, callback=stopcallback,bouncetime=200)
GPIO.add_event_detect(display, GPIO.RISING, callback=displaycallback,bouncetime=200)
