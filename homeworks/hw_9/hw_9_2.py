from machine import Pin
from time import sleep
from neopixel import NeoPixel

N = 12
p_on = Pin(15, Pin.IN, Pin.PULL_UP)

np = NeoPixel(Pin(11), N, bpp=3, timing=1)

n = 0
power_on = 0

while(1):
    if(p_on.value() == 0):
        n = min(n+1, N)
        np[n-1] = (50,0,0)
    np.write()
    sleep(0.1)

