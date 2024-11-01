from machine import Pin, Timer, ADC
from time import sleep, ticks_ms, sleep_ms
import LCD

# === Interrupts ===
led = Pin(17, Pin.OUT)
tim = Timer()
N = 0

def tic(timer):
    global N
    N += 1

tim.init(freq=1, mode=Timer.PERIODIC, callback=tic)
# tim.init(freq=1, mode=Timer.ONE_SHOT, callback=tic)

while(1):
    print(N)
    sleep_ms(100)


# === LCD Graphics ===
LCD.Init()
Navy = LCD.RGB(0,0,10)
Yellow = LCD.RGB(150,150,0)
White = LCD.RGB(255,255,255)

LCD.Clear(Navy)
LCD.Box(30, 80, 330, 150, Yellow)
LCD.Text('Hello World', 10, 50, Navy, Yellow)
LCD.Plot(x,y)
LCD.Title('Heart Rate',White, Navy)
LCD.Box(1,1, 479.319, White)
LCD.Line(5,5, 200, 200, Yellow)


# === Digital Sensors ===
