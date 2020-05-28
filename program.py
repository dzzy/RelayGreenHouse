import RPi.GPIO as GPIO
import time
import Adafruit_DHT as DHT

#set up GPIO as BCM
GPIO.setmode(GPIO.BCM)

#config values
HUMIDITY_ON = 95
HUMIDITY_OFF = 98
sleepTime = 2

#all relay pins
relayPins = [27, 22, 23]

#named GPIO pin constants
UNUSED = 17
HUMIDIFIER = 27
LIGHT = 22
FAN = 23

#sensor initialization
SENSOR = DHT.DHT22
SENSOR1 = 9
SENSOR2 = 10

# loop through relay pins and set mode and state to 'high'

print("All Relays Off")
for i in relayPins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

time.sleep(2)

#initialize variables
humidity1 = 0
humidity2 = 0
temperature1 = 0
temperature2 = 0
humidityState = "OFF"
fanState = "ON"

#start fan
GPIO.output(FAN, GPIO.LOW)
print("Enabling FAN")

try:
     while True:

          time.sleep(sleepTime)

          #read the sensor values
          humidity1a, temperature1a = DHT.read(SENSOR, SENSOR1)
          humidity2a, temperature2a = DHT.read(SENSOR, SENSOR2)


          if humidity1a is None or temperature1a is None:
               print("Failed to retrieve data from humidity sensor 1")
          else:
               humidity1 = humidity1a
               temperature1 = temperature1a

          if humidity2a is None or temperature2a is None:
               print("Failed to retrieve data from humidity sensor 2")
          else:
               humidity2 = humidity2a
               temperature2 = temperature2a

          if humidity1 is not None and temperature1 is not None:
               print("Sensor 1: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature1, humidity1))
          if humidity2 is not None and temperature2 is not None:
               print("Sensor 2: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature2, humidity2))

          humidityAvg = (humidity1 + humidity2) / 2

          if humidity1 == 0:
               humidityAvg = humidity2
               print("Sensor 1 Down: Setting humidityavg to humidity2")
          if humidity2 == 0:
               humidityAvg = humidity1
               print("Sensor 2 Down: Setting humidityavg to humidity1")
          
          temperatureAvg = (temperature1 + temperature2) / 2
          print("Humidity average: {0:0.1f}%".format(humidityAvg))
          print("Temperature average: ",temperatureAvg)

          if humidity1 is not 0 and humidity2 is not 0:
               if humidityAvg < HUMIDITY_ON:
                    if humidityState is not "ON":
                         GPIO.output(HUMIDIFIER, GPIO.LOW)
                         print("Enabling Humidifier")
                         humidityState = "ON"

               if humidityAvg > HUMIDITY_OFF:
                    if humidityState is not "OFF":
                         GPIO.output(HUMIDIFIER, GPIO.HIGH)
                         print("Disabling Humidifier")
                         humidityState = "OFF"

          else:
               print("****** Sensor failure, powering down *******")
               GPIO.output(HUMIDIFIER, GPIO.HIGH)
               GPIO.output(FAN, GPIO.HIGH)
               humidityState = "OFF"
               fanState = "OFF"

          print("Humidifier state: ",humidityState)
          print("Fan state: ",fanState)
          print("**********************************************")

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