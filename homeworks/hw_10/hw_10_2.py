from ble_simple_peripheral import BLESimplePeripheral
import bluetooth, LCD, neopixel
from machine import Pin, PWM
from math import pi
from time import sleep_ms

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

a_out = Pin(16, Pin.OUT)
a_out_pwm = PWM(a_out)
a_out_pwm.freq(20_000)

b_out = Pin(17, Pin.OUT)
b_out_pwm = PWM(b_out)
b_out_pwm.freq(20_000)
flag = 0
motor_duty = 0

def set_speed(num):
    return int((num / 100) * 65535)

def update_motor_speed(duty):
    speed = set_speed(abs(duty))
    if duty > 0:
        a_out_pwm.duty_u16(speed)
        b_out_pwm.duty_u16(0)
    else:
        a_out_pwm.duty_u16(0)
        b_out_pwm.duty_u16(speed)
    sleep_ms(10)

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
        global motor_duty
        motor_duty = int(data[0:4]) # look for 0:4 to account for negative symbol (range of +/- 100)
        motor_duty = between(motor_duty, 100)
        update_motor_speed(motor_duty)
        global flag
        flag = 1
    except:
        print('invalid data entry')

LCD.Init()
White = LCD.RGB(250,250,250)
Black = LCD.RGB(0,0,0)
Yellow = LCD.RGB(250,250,0)
LCD_reinit()
flag = 1

while(1):
    if sp.is_connected():
        sp.on_write(on_rx)
    else:
        update_motor_speed(0)

    if(flag):
        print(f'Duty Cycle: {motor_duty}%')
        LCD.Text2(str(motor_duty) + ' %  ', 320, 50, Yellow, Black)
        flag = 0
