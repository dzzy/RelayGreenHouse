import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

relays = {1:17,2:27,3:22,4:23} #outlet:gpio mapping

# loop through relays and set mode and state to 'high'

for i in relays:
    GPIO.setup(relays[i], GPIO.OUT)
    GPIO.output(relays[i], GPIO.HIGH)

# time to sleep between operations in the main loop

SleepTimeL = 1

while True:
  try:
    for i in relays:
        GPIO.output(relays[i], GPIO.LOW)
        time.sleep(5)
    for i in relays:
        GPIO.output(relays[i], GPIO.HIGH)
        time.sleep(5)
  except KeyboardInterrupt:
    # turn the relay off
    set_relay(False)
    # Reset GPIO settings
    GPIO.cleanup()
    print("\nExiting\n")
    # exit the application
    sys.exit(0)