from ds18x20 import DS18X20
from onewire import OneWire
from machine import Pin, Timer
import LCD

# LCD Colors and Init
Navy = LCD.RGB(0, 0, 10)
White = LCD.RGB(50, 50, 150)
LtBlue = LCD.RGB(150, 150, 150)
LCD.Init()
LCD.Clear(Navy)

# Temperature Sensor Setup
ds_pin = Pin(4)
ds_sensor = DS18X20(OneWire(ds_pin))
roms = ds_sensor.scan()
print('Found DS devices: ', roms)

# Timer Interrupt used for precise sampling rate
flag = 1
T = 1

def tick(timer):
    global flag
    flag = 1

Time = Timer()
Time.init(freq=1/T, mode=Timer.PERIODIC, callback=tick)

# How Good is my Coffee Cup?
# Determine the thermal time constant of your favorite cup (your pick) along with the 90% confidence interval 

# 1) Write a Python program using a DS18B20 digital thermometer.
# Use your program to determine the temperature of
# - Ice Water
# - Cold water from the tap
# - Hot water from the tap
# - Room temperature (T_amb)

def print_temp():
    ds_sensor.convert_temp()
    while True:
        while(flag == 0):
            pass
        
        print(ds_sensor.read_temp(roms[0]))
        ds_sensor.convert_temp()

# print_temp()

# 2) Write a Python program to measure and record the temperature of a hot cup of water
# - Sampling rate = 1 second
# - Duration = 2 minutes (120 samples)
# Plot your data vs. time on the graphics display

def record_temp():
    plot = [0] * 120
    file = open("out_file.txt", "a") # Also write data to file for later processing
    sec = 0
    while(sec < 120):
        while(flag == 0):
            pass
        global T
        sec += T

        temp_C = ds_sensor.read_temp(roms[0])
        ds_sensor.convert_temp()

        plot.pop()
        plot.insert(0, temp_C)
        file.write(str(sec) + ",")
        file.write(str(f"{temp_C:.2f}" + ";\n"))
        print(sec, temp_C)
        LCD.BarChart(plot, White, LtBlue)
    file.close()

# record_temp()