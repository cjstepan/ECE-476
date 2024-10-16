from machine import Pin, Timer
from time import sleep_ms

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

    def increase_interval(self):
        self.interval_ms = int(self.interval_ms * 1.01)
        self.timer.init(period=self.interval_ms, mode=Timer.PERIODIC, callback=self.buzz)
    
    def decrease_interval(self):
        self.interval_ms = int(self.interval_ms * .99)
        self.timer.init(period=self.interval_ms, mode=Timer.PERIODIC, callback=self.buzz)

    def buzz(self):
        self.buzzer.on()
        sleep_ms(self.buzz_duration_ms)
        self.buzzer.off()
