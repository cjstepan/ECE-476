from machine import Pin, I2C
from time import sleep_ms, ticks_ms
import LCD

def reg_write(i2c, addr, reg, data):
    msg = bytearray()
    msg.append(data)
    i2c.writeto_mem(addr, reg, msg)
    
def reg_read(i2c, addr, reg, nbytes=1):
    if nbytes < 1:
        return bytearray()
    data = i2c.readfrom_mem(addr, reg, nbytes)
    return data

def accel_read(reg):
    x = reg_read(i2c, addr, reg, 2)
    y = (x[0] << 8) + x[1]
    if(y > 0x8000):
        y = y - 0x10000
    y = y / 0x8000
    return(y)


i2c = I2C(0, scl=Pin(1), sda=Pin(0))

Beeper = Pin(13, Pin.OUT)
Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)

def Beep():
    Beeper.value(1)
    sleep_ms(100)
    Beeper.value(0)


# Print out any addresses found
devices = i2c.scan()
if devices:
    for d in devices:
        print('I2C Device Found:',hex(d))

addr = devices[0]
print('Communicating with ', hex(addr))

# set bandwidth
reg_write(i2c, 0x68, 0x1a, 5) # 10Hz
# set range
reg_write(i2c, 0x68, 0x1c, 0x00) # +/- 2g
RANGE = 2
# set clock freq
reg_write(i2c, 0x68, 0x6b, 0) # Internal 8MHz Clock

sleep_ms(100)

LCD.Init()
White = LCD.RGB(255,255,255)
Black = LCD.RGB(0,0,0)
Orange = LCD.RGB(255,140,0)
LCD.Clear(Black)
distance = [0,0,0]

while(1):
    is_free_fall = 0
    while(Button14.value() == 1):
        pass
    Beep()
    start_time_ms = end_time_ms = -1
    for i in range(0, 200):
        accel_z = accel_read(0x3f) * RANGE
        if accel_z < .5 and is_free_fall == 0:
            start_time_ms = ticks_ms()
            is_free_fall = 1
        if accel_z > .5 and is_free_fall == 1:
            end_time_ms = ticks_ms()
            is_free_fall = -1
        sleep_ms(10)

    jump_height_cm = .125 * 9.8 * ((start_time_ms - end_time_ms) / 1000) **2
    distance.append(jump_height_cm)
    distance.sort(reverse=True)

    
    LCD.Title('Top Jumps', White, Black)

    LCD.Text2('First Place: ', 40, 50, Orange, Black)
    LCD.Text2('Second Place: ', 40, 100, Orange, Black)
    LCD.Text2('Third Place: ', 40, 150, Orange, Black)

    sleep_ms(500)
    LCD.Text2(str(distance[0]) + ' cm ', 320, 50, White, Black)
    LCD.Text2(str(distance[1]) + ' cm ', 320, 100, White, Black)
    LCD.Text2(str(distance[2]) + ' cm ', 320, 150, White, Black)
