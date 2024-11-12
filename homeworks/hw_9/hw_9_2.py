from machine import Pin, Timer
from time import sleep_ms
from neopixel import NeoPixel
from set import Set

vars = Set(0,0,8)
start_jump = Pin(15, Pin.IN, Pin.PULL_UP)
np = NeoPixel(Pin(1), vars.N, bpp=3, timing=1)
tim = Timer()

def light(pin1):
    vars.N = 0
    np.fill([0,0,0])
    np.write()
    tim.init(freq=4,mode=Timer.PERIODIC,callback=tic)

def tic(timer):
    np.__setitem__(vars.N, [0,10,10])
    np.write()
    vars.N += 1
    if(vars.N == 7):
        tim.init(freq=4,mode=Timer.ONE_SHOT,callback=tic)
    elif vars.N == 0:
        np.fill([0,0,0])
        np.write()

start_jump.irq(trigger=Pin.IRQ_FALLING, handler=light)

while(1):
    if not vars.N == 0:
        print(vars.N)
    sleep_ms(10)

