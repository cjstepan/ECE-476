from machine import Pin, SPI
from time import sleep, sleep_us

spi = SPI(1, baudrate=10_000, polarity=0, phase=0, bits=8, sck=10, mosi=11, miso=12)

LATCH = Pin(9, Pin.OUT)
Beeper = Pin(13, Pin.OUT)
Beeper.value(0)

def LS165():
    LATCH.value(1)
    sleep_us(10)
    LATCH.value(0)
    sleep_us(10)
    LATCH.value(1)
    # data is latched - now shift it in
    rxdata = spi.read(1, 0x42)
    return(rxdata)

    
while(1):
    Y = LS165()
    print(Y)
    sleep(0.1)