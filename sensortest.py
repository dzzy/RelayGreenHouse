import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
SENSOR_PIN_1=9
SENSOR_PIN_2=10

while True:
    humidity1, temperature1 = Adafruit_DHT.read_retry(DHT_SENSOR, SENSOR_PIN_1)
    humidity2, temperature2 = Adafruit_DHT.read_retry(DHT_SENSOR, SENSOR_PIN_2)

    if humidity1 is None or temperature1 is None:
        print("Failed to retrieve data from humidity sensor 1")
    if humidity2 is None or temperature2 is None:
        print("Failed to retrieve data from humidity sensor 2")

    if humidity1 is not None and temperature1 is not None:
        print("Sensor 1: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature1, humidity1))
    if humidity2 is not None and temperature2 is not None:
        print("Sensor 2: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature2, humidity2))
    else:
        print("Failed to retrieve data from humidity sensor 2")

    time.sleep(2)