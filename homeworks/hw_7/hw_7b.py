from ds18x20 import DS18X20
from onewire import OneWire
from machine import Pin, Timer, ADC
from time import sleep, sleep_ms
from math import log, exp
import matrix # library from BisonAcademy (may need to load onto Pico)
import LCD

# LCD Colors and Init
Navy = LCD.RGB(0,0,5)
LtGreen = LCD.RGB(100,250,50)
Yellow = LCD.RGB(250,250,0)
Orange = LCD.RGB(250,150,50)
Red    = LCD.RGB(250,50,50)
Plum   = LCD.RGB(200,50,150)
White = LCD.RGB(200,200,200)
LCD.Init()
LCD.Clear(Navy)

# ADC Init
a2d4 = ADC(4)

# Temperature Sensor Setup
ds_pin = Pin(4)
ds_sensor = DS18X20(OneWire(ds_pin))
roms = ds_sensor.scan()
print('Found DS devices: ', roms)

# Timer Interrupt used for precise sampling rate
flag = 1
T = 1

def tick(timer):
    global flag
    flag = 1

Time = Timer()
Time.init(freq=1/T, mode=Timer.PERIODIC, callback=tick)


# 3) Using your data from problem #2 and Matlab, determine the thermal time constant
# of your cup using least-squares curve fitting and
# - T = be^(-at) + T_amb
# - time constant = 1/a
# -- Refer to Word doc and HW7.m for explanation


# 4) Write a Python program which uses recursive least squares to determine
# the thermal time constant of a coffee cup in real time

def coffee_cup_thermals():

    file1 = open("CoffeeCup_02.txt", "a")
    file1.write('----------------------\n')
    file1.write('Seconds  Degrees C\n')

    LCD.Box(2,2,478,318,White)
    LCD.Title('Coffee Cup', White, Navy)
    LCD.Text2('Seconds',30,60, LtGreen, Navy)
    LCD.Text2('T(cup)',30,100,Yellow,Navy)
    LCD.Text2('T(amb)',30,140,Orange,Navy)
    LCD.Text2('1/a',30,180,Red,Navy)
    LCD.Text2('b',30,220,Plum,Navy)
    time = 0
    a = 0
    b = 0

    SumX2 = 0.01
    SumX = 0
    n = 0.01
    SumXY = 0.01
    SumY = 0

    B = [[0.01,0],[0,0.01]]
    Y = [[-0.01],[0]]

    Tamb = 19.375
    alpha = 1

    while(time < 1800):
        while(flag == 0):
            pass
        flag = 0
        ds_sensor.convert_temp()
        sleep_ms(750)
        Temp = ds_sensor.read_temp(roms[0])  
        
        x = time
        y = log(Temp - Tamb)
        
    #    B = matrix.mult_k(B, alpha)
    #    Y = matrix.mult_k(Y, alpha)
        
        B = matrix.add(B, [[x**2, x], [x, 1]])
        Y = matrix.add(Y, [[x*y], [y]])
        
        Bi = matrix.inv(B)
        A = matrix.mult(Bi, Y)
        if(A[0][0] != 0):
            a = -1 / A[0][0]
        else:
            a = 0
        b = exp(abs(A[1][0]))
        
        print(time, Temp, a, b)

        if(( int(time) % 10) == 0):
            file1.write(str('{: 4.0f}'.format(time)) + " ")
            file1.write(str('{: 7.4f}'.format(Temp)) + " ")
            file1.write(str('{: 7.4f}'.format(Tamb)) + " ")
            file1.write(str('{: 9.4f}'.format(a)) + " ")
            file1.write(str('{: 7.4f}'.format(b)) + " ")
            file1.write("\n")

        LCD.Number2(time, 9, 1, 200, 60, LtGreen, Navy)
        LCD.Number2(Temp, 9, 3, 200, 100, Yellow, Navy)
        LCD.Number2(Tamb, 9, 3, 200, 140, Orange, Navy)
        LCD.Number2(a, 9, 3, 200, 180, Red, Navy)
        LCD.Number2(b, 9, 3, 200, 220, Plum, Navy)

        time += T

    file1.close()


# 5) With this program, record the thermal time constant for a given cup three times
# From your data determine the 90% confidence interval for the actual thermal time constant
# - student t-test
# -- Refer to word document and 

