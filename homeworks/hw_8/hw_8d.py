# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-bme280-micropython/

from machine import Pin, I2C
from time import sleep
import BME280

# === Weather Station ===
# Use a BME280 sensor to measure temperature, humidity, and air pressure
# - Display this data on the screen

# 6) Write a Python program to read a BME280 sensor. Display as text on the LCD display
# - Temperature
# - Humidity
# - Air pressure

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)

while True:
    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c)
        
        # Read sensor data
        tempC = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        
        # Print sensor readings
        print('---------')
        print('Temperature: ', tempC)
        print('Humidity: ', hum)
        print('Pressure: ', pres)
        
    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

    sleep(5)
