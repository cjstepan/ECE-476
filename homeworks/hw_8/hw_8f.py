# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-bme280-micropython/

from machine import Pin, I2C
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
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)

# Initialize GP15 as push button
toggle_btn = Pin(15, Pin.IN, Pin.PULL_UP)

show_plot = 0
def toggle(btn):
    global show_plot
    show_plot += 1

toggle_btn.irq(handler=toggle, trigger=Pin.IRQ_FALLING)

# LCD Init
Navy = LCD.RGB(0,0,5)
White = LCD.RGB(200,200,200)
Yellow = LCD.RGB(200,200,0)
LCD.Init()
LCD.Clear(Navy)


time, data_tempC, data_humidity, data_pressure = []
for i in range(0,60):

    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c)
        
        # Read sensor data
        tempC = bme.temperature
        hum = bme.humidity
        pres = bme.pressure

        # Record sensor data
        data_tempC.append(tempC)
        data_humidity.append(hum)
        data_pressure.append(pres)
        
    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

sleep(1)
while True:

    LCD.Clear(Navy)

    if show_plot == 0:
        LCD.Title("Temp C", White, Navy)
        LCD.Plot(time, data_tempC)
    elif show_plot == 1:
        LCD.Title("Humidity", White, Navy)
        LCD.Plot(time, data_humidity)
    elif show_plot == 2:
        LCD.Title("Pressure", White, Navy)
        LCD.Plot(time, data_pressure)
    else:
        show_plot = 0