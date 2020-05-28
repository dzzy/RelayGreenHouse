import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

pinList = [17, 27, 22, 23]

# loop through pins and set mode and state to 'high'

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

# time to sleep between operations in the main loop

SleepTimeL = 1


try:
  print ("ONE ON")
  time.sleep(SleepTimeL)
  GPIO.output(27, GPIO.LOW)
  print ("TWO ON")
  time.sleep(SleepTimeL)
  GPIO.output(22, GPIO.LOW)
  print ("THREE ON")
  time.sleep(SleepTimeL)
  GPIO.output(23, GPIO.LOW)
  print ("FOUR ON")
  time.sleep(SleepTimeL)
  GPIO.output(17, GPIO.LOW)
except KeyboardInterrupt:
  # turn the relay off
  set_relay(False)
    # Reset GPIO settings
  GPIO.cleanup()
  print("\nExiting\n")
  # exit the application
  sys.exit(0)