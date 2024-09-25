from machine import Pin, PWM, ADC
from time import sleep_ms
import LCD

a_out = Pin(16, Pin.OUT)
a_out_pwm = PWM(a_out)
a_out_pwm.freq(20_000)

b_out = Pin(17, Pin.OUT)
b_out_pwm = PWM(b_out)
b_out_pwm.freq(20_000)

button = Pin(15, Pin.IN, Pin.PULL_UP)

# 1) Write a Python program which
# Allows you to input a number from -100 to +100, and
# Outputs a PWM signal to control the speed of a DC servo motor
# Test your code: Shown in control_motor.mp4
def set_speed(num):
    return int((num / 100) * 65535)

def control_motor():
    number = int(input("Enter a Number [-100, 100]: "))
    speed = set_speed(abs(number))

    while(1):
        if number > 0:
            a_out_pwm.duty_u16(speed)
            b_out_pwm.duty_u16(0)
        else:
            a_out_pwm.duty_u16(0)
            b_out_pwm.duty_u16(speed)
        if not button.value():
            number = int(input("Enter a Number [-100, 100]: "))
            speed = set_speed(abs(number))
        sleep_ms(10)

# control_motor()

# 2) Write a Python program which
# Reads the analog joystick and
# Returns a number from -100 to +100 as you move the joystick up and down
# Tested in read_analog.mp4
def read_analog():
    a2d1 = ADC(1)
    return int(((a2d1.read_u16() - 65535 / 2) / (65535 / 2))*(100))

def read_joystick():
    while(1):
        print(read_analog())
        sleep_ms(100)

# read_joystick()

# 3) Write a Python program which displays on the graphics display
# The speed of the motor (0 to +100)
# The direction (CW of CCW), and
# The joystick position as a bar-graph
# Tested in run_graphics.mp4
def run_graphics():
    Navy = LCD.RGB(0,0,10)
    Cyan = LCD.RGB(0,150,150)
    LtBlue = LCD.RGB(50,50,150)
    White = LCD.RGB(150,150,150)

    LCD.Init()
    LCD.Clear(Navy)

    joystick_reads = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for speed_number in range(-100,100):
        joystick_reads.insert(0, read_analog() + 100)
        joystick_reads.pop()
        LCD.Text(f'Speed: {abs(speed_number)}    Direction: {"CW  " if speed_number > 0 else "CCW "}',5,5,Cyan,Navy)
        LCD.BarChart(joystick_reads, White, LtBlue)
        sleep_ms(1)

# run_graphics()

# 4) Put these all together for a Python program to control and display 
# the speed and direction of a DC motor.

def motor_display():
    Navy = LCD.RGB(0,0,10)
    Cyan = LCD.RGB(0,150,150)
    LtBlue = LCD.RGB(50,50,150)
    White = LCD.RGB(150,150,150)

    LCD.Init()
    LCD.Clear(Navy)

    joystick_reads = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for speed_number in range(-100,100):
        speed = set_speed(abs(read_analog()))
        if read_analog() > 0:
            a_out_pwm.duty_u16(speed)
            b_out_pwm.duty_u16(0)
        else:
            a_out_pwm.duty_u16(0)
            b_out_pwm.duty_u16(speed)
        
        joystick_reads.insert(0, read_analog() + 100)
        joystick_reads.pop()
        LCD.Text(f'Speed: {abs(speed_number)}    Direction: {"CW  " if speed_number > 0 else "CCW "}',5,5,Cyan,Navy)
        LCD.BarChart(joystick_reads, White, LtBlue)
        sleep_ms(1)

motor_display()
# 5) Demo your program. Tested in motor_display.mp4