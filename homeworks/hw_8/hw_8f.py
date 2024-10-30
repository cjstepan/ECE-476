# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-bme280-micropython/

from machine import Pin, I2C, Timer
from time import sleep
import BME280
import LCD

# === Weather Station ===
# Use a BME280 sensor to measure temperature, humidity, and air pressure
# - Display this data on the screen

# 8) Modify this program to display each of these data sets as a graph on the LCD display,
# - Start with displaying temperature for 60 seconds
# - Each time you press GP15, you switch to the next data set (Temperature >> humidity >> pressure
# >> repeat)
# - Give the results after one minute of data collection (60 points)

# 9) Demonstrate your program
# - In-person or video

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(9), sda=Pin(8), freq=10000)

# Initialize BME280 sensor
bme = BME280.BME280(i2c=i2c, addr=0x76)

# Initialize GP15 as push button
toggle_btn = Pin(15, Pin.IN, Pin.PULL_UP)

# LCD Init
Navy = LCD.RGB(0,0,5)
White = LCD.RGB(200,200,200)
Yellow = LCD.RGB(200,200,0)
LCD.Init()
LCD.Clear(Navy)

time = []
data_tempC = []
data_humidity = []
data_pressure = []
i = 0
while i < 60:
    time.append(i)
    # Read sensor data
    tempC = float(bme.temperature[:5])
    hum = float(bme.humidity[:5])
    pres = float(bme.pressure[:6])

    # Record sensor data
    data_tempC.append(tempC)
    data_humidity.append(hum)
    data_pressure.append(pres)

sleep(1)
show_plot = 0
while True:
    while toggle_btn.value():
        pass
    LCD.Clear(Navy)

    if show_plot == 0:
        LCD.Title("Temp C", White, Navy)
        LCD.Plot(time, data_tempC)
        show_plot = 1
    elif show_plot == 1:
        LCD.Title("Humidity", White, Navy)
        LCD.Plot(time, data_humidity)
        show_plot = 2
    else:
        LCD.Title("Pressure", White, Navy)
        LCD.Plot(time, data_pressure)
        show_plot = 0