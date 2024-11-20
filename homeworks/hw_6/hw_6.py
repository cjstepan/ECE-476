from machine import Pin, Timer
from time import sleep_ms

# Build a metronome with your Pi-Pico. Output a 10ms beep every N ms
# On startup, N = 1000ms (60 beats per minute)
# Increase N by 1% each time you press GP15
# Decrese N by 1% each time you press GP14
# Display beats per minute on the graphics display

# 1) Write a Python program which outputs a 10ms pulse every 1000ms using Timer interrupts
# -Test your program
# -(100ms pulse should read 0.33V, 200ms pulse should read 0.66V, ticks_us() should read 1000000 micro-seconds between beeps)

# 2) Write a Python program which uses edge interrupts to
# -Increase a number by 1% each time you press GP15
# -Decrease a number by 1% each time you press GP14
# -Test your code with N starting at 1000

# 3) Write a Python program which uses timer and edge interrupts to build a metronome
# -Test your program

# 4) Demo your metronome
# -See Attached Video in Folder

class Metronome:
    """The Metronome class holds all the corresponding functions to operate the metronome."""
    
    buzzer = Pin(13, Pin.OUT)
    increase_btn = Pin(15, Pin.IN, Pin.PULL_UP)
    decrease_btn = Pin(14, Pin.IN, Pin.PULL_UP)
    
    timer = Timer()
    interval_ms = 1000 # ms (60bpm)
    buzz_duration_ms = 10

    def __init__(self):
        self.timer.init(period=self.interval_ms, mode=Timer.PERIODIC, callback=self.buzz)
        self.increase_btn.irq(trigger=Pin.IRQ_FALLING, handler=self.increase_interval)
        self.decrease_btn.irq(trigger=Pin.IRQ_FALLING, handler=self.decrease_interval)

    def increase_interval(self, pin):
        self.interval_ms = int(self.interval_ms * 1.01)
        self.timer.init(period=self.interval_ms, mode=Timer.PERIODIC, callback=self.buzz)
    
    def decrease_interval(self, pin):
        self.interval_ms = int(self.interval_ms * .99)
        self.timer.init(period=self.interval_ms, mode=Timer.PERIODIC, callback=self.buzz)

    def buzz(self, timer):
        self.buzzer.on()
        sleep_ms(self.buzz_duration_ms)
        self.buzzer.off()
        print(self.interval_ms)
Metronome()
