import includes.py
import definitions.py
import functions.py

#set GPIO pin mode
GPIO.setmode(GPIO.BCM)

for i in Sockets: #set up the socket GPIO pins
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

for i in Sensors: #set up the sensors
    #configure sensors

try: #main try statement

    while True:  #main while loop, endless looping
        
        time.sleep(SleepTime) #sleepy sleep save da cpu

        #get time
        time = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("current time" + current_time)

        #determine if any time-based parameters need changing
        

        #check sensor values

        #determine if any sensor-based parameters need changing

# End program cleanly with keyboard
except KeyboardInterrupt:
  print ("  Quit")

  # Reset GPIO settings
  GPIO.cleanup()

