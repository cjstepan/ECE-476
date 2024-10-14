from machine import Pin, Timer
from time import sleep_ms

# Build a metronome with your Pi-Pico. Output a 10ms beep every N ms
# On startup, N = 1000ms (60 beats per minute)
# Increase N by 1% each time you press GP15
# Decrese N by 1% each time you press GP14
# Display beats per minute on the graphics display

led = Pin(17, Pin.OUT)
increase_btn = Pin(15, Pin.IN, Pin.PULL_UP)
decrease_btn = Pin(14, Pin.IN, Pin.PULL_UP)
tim = Timer()
N = 1000 # ms/60bpm

# 1) Write a Python program which outputs a 10ms pulse every 1000ms using Timer interrupts
# -Test your program
# -(100ms pulse should re ad 0.33V, 200ms pulse should read 0.66V, ticks_us() should read 1000000 micro-seconds between beeps)
def pulse(timer):
    global N
    N += 1

tim.init(freq=1, mode=Timer.PERIODIC, callback=pulse)

while(1):
    print(N)
    sleep_ms(100)