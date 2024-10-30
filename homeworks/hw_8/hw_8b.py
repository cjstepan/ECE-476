from machine import Pin, ADC, Timer
from time import sleep
import LCD

# === Heart Sensor ===
# Write a Python program which
# - Uses the Heart & Pulse sensor to record your pulse
# - Detects each pulse automatically,
# - Computes your heart rate in beats-per-minute, and
# - Displays your pulse as a graph on the graphics display as well as your beats-per-minute.

# 2) Write a Python program which detects each beat
# - Flash an LED for 100ms each pulse
# - Beep the beeper for 100ms each pulse

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
    for i in range(0,1000):
        while(flag == 0):
            pass
        flag = 0

        Volts = (a2d2.read_u16() * kV)
        print(Volts)
        x[i] = i    
        y[i] = Volts
    
    if Volts > 1.7:
        beeper.on()
        led.on()
    else:
        beeper.off()
        led.off()

    Navy = LCD.RGB(0,0,5)
    White = LCD.RGB(200,200,200)
    LCD.Clear(Navy)
    LCD.Plot(x,y)
    LCD.Title('Heart Rate',White, Navy)

    sleep(1)