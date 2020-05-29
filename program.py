import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
import time
import datetime

#config values
HUMIDITY_ON = 95
HUMIDITY_OFF = 98
sleepTime = 3
errorResetRate = 300 / sleepTime # seconds / sleeptime, 5 minutes. if we dont get a value from one sensor for 5 minutes the average will reset to the other sensor


#all relay pins
relayPins = [17, 27, 22, 23]

#relay GPIO pins
UNUSED = 17
HUMIDIFIER = 27
LIGHT = 22
FAN = 23

#sensor GPIO pins
SENSOR = DHT.DHT22
SENSOR1 = 9
SENSOR2 = 10

#set up GPIO as BCM
GPIO.setmode(GPIO.BCM)

# loop through relay pins and set mode and state to 'high'
print("Program Start: All Relays Off")
for i in relayPins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

time.sleep(sleepTime)

#initialize variables
humidity1 = 0
humidity2 = 0
temperature1 = 0
temperature2 = 0
error1 = 0
error2 = 0
loopCount = 0
humidityState = "OFF"
fanState = "ON"
lightState = "OFF"

#start fan
GPIO.output(FAN, GPIO.LOW)
print("**** Enabling FAN ****")

#turn on light
GPIO.output(LIGHT, GPIO.LOW)
print("**** Enabling Light ****")
lightState = "ON"

try:
     while True:

          #sleepyTime
          time.sleep(sleepTime)

          #loopCount
          loopCount += 1

          #get the current time
          timeString = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time()))
          currentTime = datetime.strftime(datetime.utcnow(),"%H:%M:")

          #read the sensor values to temp a variables
          humidity1a, temperature1a = DHT.read(SENSOR, SENSOR1)
          humidity2a, temperature2a = DHT.read(SENSOR, SENSOR2)

          if humidity1a is None or temperature1a is None: 
               print("**** Failed to retrieve data from humidity sensor 1 ****")
               error1 += 1
               if error1 > errorResetRate: #if we get more than errorResetRate sensor read errors on sensor 1
                    humidity1 = humidity2 #store the current value of sensor 2 into humidity1 to get a more accurate average
                    error1 = 0 #and reset the error rate
                    print("**** Resetting sensor 1 errors to sensor 2 ****")

          else: #we got a good reading, set variables for averaging
               humidity1 = humidity1a
               temperature1 = temperature1a

          if humidity2a is None or temperature2a is None: 
               print("**** Failed to retrieve data from humidity sensor 2 ****")
               error2 += 1
               if error2 > errorResetRate: #if we get more than errorResetRate sensor read errors on sensor 2
                    humidity2 = humidity1 #store the current value of sensor 1 into humidity2 to get a more accurate average
                    error2 = 0 #and reset the error rate
                    print("**** Resetting sensor 1 errors to sensor 2 ****")
          else:
               #otherwise, we got a good reading and store it into the humidity2 variable
               humidity2 = humidity2a
               temperature2 = temperature2a

          if loopCount == errorResetRate:
               error1 = 0
               error2 = 0
               print("**** Resetting Error Rate ****")

          #calculate average humidity
          humidityAvg = (humidity1 + humidity2) / 2

          #calculate average temperature          
          temperatureAvg = (temperature1 + temperature2) / 2

          #output the status
          print("Current Time:           ",timeString)
          print("Sensor 1 Temp:          {0:0.1f}*C  Humidity={1:0.1f}%".format(temperature1, humidity1))
          print("Sensor 2 Temp:          {0:0.1f}*C  Humidity={1:0.1f}%".format(temperature2, humidity2))
          print("Humidity average:       {0:0.1f}%".format(humidityAvg))
          print("Temperature average:    {0:1.2f}*C".format(temperatureAvg))
          print("Humidifier state:       ",humidityState)
          print("Humidifier last change: ",humidifierChange)
          print("Fan state:              ",fanState)
          print("Light state:            ",lightState)

          if humidityAvg < HUMIDITY_ON and humidityState is not "ON": #if humidity is less than the on trigger, enable humidifier
               GPIO.output(HUMIDIFIER, GPIO.LOW)
               print("**** Enabling Humidifier ****")
               humidityState = "ON"
               humidifierChange = timeString

          if humidityAvg > HUMIDITY_OFF and humidityState is not "OFF": #if humidity is more than the cutoff, turn off. 
               GPIO.output(HUMIDIFIER, GPIO.HIGH)
               print("**** Disabling Humidifier ****")
               humidityState = "OFF"
               humidifierChange = timeString

          if humidity1 == 0 and humidity2 == 0: #both sensors are 0. turn off and exit. 
               print("**** Sensor failure, powering down ****")
               GPIO.output(HUMIDIFIER, GPIO.HIGH)
               GPIO.output(FAN, GPIO.HIGH)
               humidityState = "OFF"
               fanState = "OFF"
               break

          print("................................................................")

except KeyboardInterrupt:
     # turn the relay off
     print("Cleanup")
     for i in relayPins:
          GPIO.setmode(GPIO.BCM)
          GPIO.output(i, GPIO.HIGH)
          GPIO.cleanup()
     # Reset GPIO settings
     print("\nExiting\n")
     # exit the application
     sys.exit(0)