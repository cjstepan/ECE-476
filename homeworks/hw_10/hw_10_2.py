from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import neopixel
import LCD
from set import Set

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

np = neopixel.NeoPixel(Pin(1), 8, bpp=3, timing=1) # 8 Neopixels

vars = Set(0,0,0)

def set_neopixel(value):
    vars.Level = value
    np.fill([vars.Level,vars.Level,vars.Level])
    np.write()

def LCD_reinit():
    LCD.Clear(Black)
    LCD.Text2('Duty Cycle: ', 50, 50, Yellow, Black)
    LCD.Title('Bluetooth Motor Control', White, Black)
    
def between(num, bound):
    if num > bound:
        num = bound
    elif num < -bound:
        num = -bound
    return num

def on_rx(data):
    print("Data received: ", data)
    try:
        vars.Level = int(data[0:4]) # look for 0:4 to account for negative symbol (range of +/- 100)
        vars.Level = between(vars.Level, 100)
        set_neopixel(vars.Level)
        vars.flag = 1
    except:
        print('invalid data entry')

LCD.Init()
White = LCD.RGB(250,250,250)
Black = LCD.RGB(0,0,0)
Yellow = LCD.RGB(250,250,0)
LCD_reinit()
vars.flag = 1

while(1):
    if sp.is_connected():
        sp.on_write(on_rx)
    elif not sp.is_connected() and not vars.Level == 0:
        LCD_reinit()
        vars.Level = 0
    else:
        set_neopixel(vars.Level)
        
    if(vars.flag):
        print(f'Duty Cycle: {vars.Level}%')
        LCD.Text2(str(vars.Level) + ' %  ', 320, 50, Yellow, Black)
        vars.flag = 0
