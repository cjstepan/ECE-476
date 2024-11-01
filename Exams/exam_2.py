# === Problem 1 ===
from machine import Pin, Timer
from time import sleep_ms

tim = Timer()
Buzzer = Pin(0, Pin.OUT) # Assuming GP0 is Pin 0

global play
play = 1

def buzz(timer):
    if play == 1:
        if flag == 0:
            Buzzer.on()
            flag = 1
        else:
            Buzzer.off()
            flag = 1
    else:
        Buzzer.off()

def BuzzerOff(pin1):
    Buzzer.off()
    play = 0

tim.init(freq=220, mode=Timer.PERIODIC, callback=buzz)

tim.init(freq=1.333, mode=Timer.ONE_SHOT,callback=BuzzerOff) # 1/750ms = 1.333hz

while True:
    sleep_ms(500)


# === Problem 2 ===
from machine import Pin, PWM
from time import sleep_ms


led = Pin(16, Pin.OUT)
led = PWM(Pin(16))
led.freq(100)
led.duty_u16(0)
# < 20C = 0%
# 20 - 40C = 0-100%
# > 40C = 100%
def AnalogSensor_to_PWM(degc):
    duty_cycle_percent = -1 # to check for error
    if degc < 20:
        duty_cycle_percent = 0
    elif degc >= 20 and degc <= 40:
        duty_cycle_percent = (5 * (degc - 20)) / 100 # to scale the temperature accordingly
        led.duty_u16(duty_cycle_percent * 65535)
    else:
        duty_cycle_percent = 100


# === Problem 3 ===
from machine import Pin
from math import log, e
import random
from time import sleep

buzzer = Pin(13, Pin.OUT)

def buzz():
    buzzer.on()
    sleep(.1)
    buzzer.off()

def get_interval():
    p = random.randrange(0,1)
    x = -10 * log(1-p)

    return x

while True:
    buzz()
    x = get_interval()
    sleep(x)


# === Problem 4 ===
from machine import Pin
from time import ticks_ms

led = Pin(0, Pin.IN, Pin.PULL_DOWN)
btn = Pin(1, Pin.IN, Pin.PULL_UP)

global start_time, end_time
start_time, end_time = -1

def record_time_led():
    start_time = ticks_ms()

def record_time_btn():
    end_time = ticks_ms()
    print(f'Time Difference={start_time - end_time}ms')

led.irq(trigger=Pin.IRQ_RISING, handler=record_time_led)
btn.irq(trigger=Pin.IRQ_FALLING, handler=record_time_btn)

while True:
    pass