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

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

#channels for sensors
light_channel = 0
temp_channel = 1
pot_channel = 2


# Channels for sensors
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)  
  return volts
  
# Function to calculate temperature from MCP9700E data
def ConvertTemp(data):
    
  temp = int((data-0.5)*100)
  return temp

# Function to calculate LIGHT from LDR data
def ConvertLight(data):
    light = int((data/3.1*100))
    return light

# Function to return correct time format
def timeFormat(t):
    timeinstance=time.localtime(t)
    return(str(timeinstance.tm_min).zfill(2)+":"+str(timeinstance.tm_sec).zfill(2)+":"+str(t-int(t))[2:4])
 

# interrupt to change frequency
def freqcallback(channel):
    global delay
    if delay == 0.5:
        delay = 1
    elif delay == 1:
        delay = 2
    elif delay == 2:
        delay = 0.5

# interrupt to reset timer
def resetcallback(channel):
    global starttime
    global log
    global log_count
    
    starttime = time.time()
    log = ""
    logcount = 0
    os.system('clear')

