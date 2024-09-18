from machine import Pin
from time import sleep_ms, sleep_us

CLK = Pin(10, Pin.OUT)
DIN = Pin(12, Pin.IN, Pin.PULL_UP)
LATCH = Pin(9, Pin.OUT)

def HC165():
    LATCH.value(1)
    CLK.value(1)
    sleep_ms(100)
    LATCH.value(0)
    sleep_ms(100)
    LATCH.value(1)
    # data is latched - now shift it in
    X = 0
    for i in range(0,8):
        CLK.value(0)
        sleep_ms(100)
        X = (X << 1) + DIN.value()
        CLK.value(1)
        sleep_ms(100)
        print(i, X)
    return(X)
    
while(1):
    Y = HC165()
    print(Y)
    sleep_ms(100)