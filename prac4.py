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


#initializing variables

delay = 1
monitor = 1
starttime =time.time()
log_count = 0
log =""
logA =""


while True:

  # Read the light sensor data
  light_level = ReadChannel(light_channel)
  light_volts = ConvertVolts(light_level,2)
  light       = ConvertLight(light_volts)

  # Read the temperature sensor data
  temp_level = ReadChannel(temp_channel)
  temp_volts = ConvertVolts(temp_level,2)
  temp       = ConvertTemp(temp_volts)
  
  # Read voltage on pot
  pot_level =ReadChannel(pot_channel)
  pot_volts = ConvertVolts(pot_level,2)
  #print(pot_volts)
  
  
  logA = timeFormat(time.time())+" "+timeFormat(time.time()-starttime)+" "+"{}V {}C {}%".format(pot_volts,temp,light)
  
  if(monitor ==1):
      print("Time     Timer    pot   Temp  Light")
      print(logA)
      
  elif(monitor == 0 and log_count<5):
      log = log+"\n"+logA
      log_count= log_count+1

  # Wait before repeating loop
  time.sleep(delay)


