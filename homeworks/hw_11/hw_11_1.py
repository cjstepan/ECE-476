from machine import Pin, I2C
from time import sleep
from neopixel import NeoPixel

np = NeoPixel(Pin(11), 8, bpp=3, timing=1)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
Beeper = Pin(13, Pin.OUT)
clear_tree_btn = Pin(14, Pin.IN, Pin.PULL_UP)
start_race_btn = Pin(15, Pin.IN, Pin.PULL_UP)

def clear_strip():
    np.fill([0,0,0])
    np.write()

def Beep():
    Beeper.value(1)
    sleep(.1)
    Beeper.value(0)

clear_strip()
while(1):
    if (clear_tree_btn.value() == 0):
        clear_strip()
        print("Starter Tree Cleared")
        Beep()
        sleep(.1)
        Beep()
    if(start_race_btn.value() == 0):
        Beep()
        clear_strip()
        for i in reversed(range(8)):
            rgb_value = int((1/(i+1))*125)
            print(rgb_value, i)
            np.__setitem__(i, [rgb_value,rgb_value,0])
            np.write()
            sleep(1)
        np.fill([0,200,0])
        np.write()
        Beep()
        print("Race Started")
