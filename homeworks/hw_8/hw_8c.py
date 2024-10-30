from machine import Pin, ADC, Timer
from time import sleep, ticks_us
import LCD

# === Heart Sensor ===
# Write a Python program which
# - Uses the Heart & Pulse sensor to record your pulse
# - Detects each pulse automatically,
# - Computes your heart rate in beats-per-minute, and
# - Displays your pulse as a graph on the graphics display as well as your beats-per-minute.

# 3) Write a Python program which measures the time between pulses with a resolution of 1us
# - Display the results on the terminal window
# - Give the results of your program

# 4) Modify this program to output on the graphics display
# - The measured pulse signal as a graph
# - The time between pulses in micro-seconds, and
# - Your beats-per-minute, with a resolution of 0.01bpm

# 5) Demonstrate your progam

flag = 1
T = 0.0025

led = Pin(16, Pin.OUT)
beeper = Pin(13, Pin.OUT)

def tick(timer):
    global flag
    flag = 1

Time = Timer()
Time.init(freq=1/T, mode=Timer.PERIODIC, callback=tick)

a2d2 = ADC(2)
kV = 3.3 / 65535

Navy = LCD.RGB(0,0,5)
Yellow = LCD.RGB(200,200,0)
LCD.Init()
LCD.Clear(Navy)
time = 0


x = [0]*1000
y = [0]*1000

LCD.Init()

while(1):   
    
    last_beat_tick = -100
    beats = 0
    start_time = ticks_us()

    for i in range(0,1000):
        while(flag == 0):
            pass
        flag = 0

        Volts = (a2d2.read_u16() * kV)
        x[i] = i    
        y[i] = Volts
    
    if Volts > 1.7 or i < last_beat_tick + 100:
        beeper.on()
        led.on()
        if i > last_beat_tick + 100:
            beats += 1
            last_beat_tick = i
    else:
        beeper.off()
        led.off()
    end_time = ticks_us()

    pulse_time = end_time - start_time
    bpm = beats / ((pulse_time) / 60000000)
    print(f'Time Between Pulses={pulse_time}')

    Navy = LCD.RGB(0,0,5)
    White = LCD.RGB(200,200,200)
    LCD.Clear(Navy)
    LCD.Plot(x,y)
    LCD.Title('Heart Rate',White, Navy)
    LCD.Text(f'BPM={bpm:.2f}', 25, 7, Navy, Yellow)
    LCD.Text(f'Time={pulse_time:.2f}us', 325, 7, Navy, Yellow)

    sleep(1)