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

