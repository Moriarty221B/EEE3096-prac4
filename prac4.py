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
  
  # Print out results
  #print( "--------------------------------------------"  )
  #print("Light : {} ({}%)".format(light_level,light_percent))  
  #print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
  #print(pot_volts)
  #print(timerT)
  #timerT = timmer(timerT,delay)
  #print(timerT)
  #delay = delay_setter(delay)
  #print(delay)
  #print(datetime.datetime.now().strftime('%H:%M:%S'))
  

  # Wait before repeating loop
  time.sleep(delay)

