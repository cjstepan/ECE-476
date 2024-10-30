# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-bme280-micropython/

from machine import Pin, I2C, Timer
from time import sleep
import BME280

# === Weather Station ===
# Use a BME280 sensor to measure temperature, humidity, and air pressure
# - Display this data on the screen

# 7) Modify this program to record temperature, pressure, and humidity for one minute with a sampling
# rate of one second (60 data points). After one second, display the data on the terminal window.

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(9), sda=Pin(8), freq=10000)

# Timer Init
tim = Timer()
N = 0

def tic(timer):
    global N
    N += 1

tim.init(freq=1, mode=Timer.PERIODIC, callback=tic)

while N < 60:
    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c)
        
        # Read sensor data
        tempC = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        
        # Print sensor readings
        if N > 0:
            print('---------')
            print('Temperature: ', tempC)
            print('Humidity: ', hum)
            print('Pressure: ', pres)
        
    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)
