# Timer2 Interrupts:
Hz = 327.63
N0 = 10_000_000 / (2*Hz)
print('Target N = ',N0)
A, B, C = 0, 0, 0
MinError = 9999
for a in range(1,17):
    for b in range(1,257):
        for c in [1, 4, 16]:
            N = a*b*c
            Error = abs(N - N0)
            if(Error < MinError):
                A = a
                B = b
                C = c
                MinError = Error
print('A = ',A)
print('B = ',B)
print('C = ',C)
print('N = ',A*B*C)


# Convolution with Dice:
def linspace(x0, dx, x1):
    x = x0
    A = []
    while(x <= x1):
        A.append(x)
        x += dx

def display(A):
    n = len(A)
    for k in range(0,n):
        print('{: 4.0f}'.format(k),'{: 10.3f}'.format(A[k]))

def uniform(a,b):
    A = []
    N = b-a+1
    for i in range(0,a):
        A.append(0)
    for i in range(a,b+0.01):
        A.append(1/N)
    return(A)

def conv(A, B):
    nA = len(A)
    nB = len(B)
    nC = nA + nB - 1
    C = []
    for n in range(0,nC):
        C.append(0)
        for k in range(0,nA):
            if(((n-k)>=0)&((n-k)<nB)&(k<nA)):
                C[n] += A[k]*B[n-k]
    return(C)

d4 = uniform(1,4)
d6 = uniform(1,6)
d4d6 = conv(d4,d6)
print('d4 + d6')
display(d4d6)


# Morse Code
from machine import Pin
from time import sleep_ms

Beeper = Pin(13, Pin.OUT)

def Dit():
    Beeper.value(1)
    sleep_ms(100)
    Beeper.value(0)
    sleep_ms(100)

def Dah():
    Beeper.value(1)
    sleep_ms(300)
    Beeper.value(0)
    sleep_ms(100)

def Pause():
    sleep_ms(300)


# Voting Machine 
# input 14 and 15

from machine import Pin
from time import sleep_ms

PlayerA = Pin(15, Pin.IN, Pin.PULL_UP)
PlayerB = Pin(14, Pin.IN, Pin.PULL_UP)

A = 1
B = 1
Na = 0
Nb = 0
time = 0
while(1):
    zA = A
    A = PlayerA.value()
    zB = B
    B = PlayerB.value()
    if( (A==1) & (zA==0) ):
        Na += 1
    if( (B==1) & (zB==0) ):
        Nb += 1
    print('Votes for A ',Na, '   Votes for B ',Nb)
    sleep_ms(100)


# HC165 Bitbanging
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


# 3-Key Piano
import time
from machine import Pin, PWM

Spkr = PWM(Pin(18))
B0 = Pin(20, Pin.IN, Pin.PULL_UP)
B1 = Pin(21, Pin.IN, Pin.PULL_UP)
B2 = Pin(22, Pin.IN, Pin.PULL_UP)

while(1):
    if(B0.value() == 0):
        Spkr.freq(220)
        Spkr.duty_u16(32768)
        while(B0.value() == 0):
            pass
    if(B1.value() == 0):
        Spkr.freq(250)
        Spkr.duty_u16(32768)
        while(B1.value() == 0):
            pass
    if(B2.value() == 0):
        Spkr.freq(280)
        Spkr.duty_u16(32768)
        while(B2.value() == 0):
            pass
    pwm.duty_u16(0)


# PWM
from time import sleep_ms
from machine import Pin, PWM

LED = Pin(17, Pin.OUT)
LED = PWM(Pin(17))
LED.freq(100)

x = 0
dx = 100
    
while(1):
    x += dx
    LED.duty_u16(x)
    if(x > 65000):
        dx = -abs(dx)
    if(x <= 0):
        dx = abs(dx)
    sleep_ms(1)


# A2D Read
from machine import ADC
from time import sleep_ms

a2d0 = ADC(0)
a2d1 = ADC(1)

while(1):
    x = a2d0.read_u16() >> 4 
    y = a2d1.read_u16() >> 4 

    print(x, y)
    sleep_ms(200)


# Temperature Read
from machine import ADC
from time import sleep_ms

a2d0 = ADC(0)
a2d1 = ADC(1)
a2d4 = ADC(4)

k = 3.3 / 65520

while(1):
    a0 = a2d0.read_u16()
    a1 = a2d1.read_u16() 
    a4 = a2d4.read_u16()

    V0 = a0 * k
    V1 = a1 * k
    Temp = 0.02927*(14940 - a4)

    print(V0, V1, Temp)
    sleep_ms(200)


# Voltage Read
from machine import ADC
from time import sleep_ms

a2d2 = ADC(2)

k = 20.0 / 65520

while(1):
    a2 = a2d2.read_u16()
    V2 = k * (a2 - 32767)

    print(V2, ' Volts')
    sleep_ms(200)


# PWM Out
from machine import Pin, PWM
from time import sleep_ms
from math import sin, pi

Aout = Pin(16, Pin.OUT)
Aout = PWM(Pin(16))
Aout.freq (1000)

Table = []
for i in range(0,100):
    Table.append(int(65535*sin(i*pi/100)))
for i in range(0,100):
    Table.append(0)

i = 0
while(1):
    i = (i + 1) % 200
    Aout.duty_u16(Table[i])
    sleep_ms(10)


# Full Stepping
# Stepper Motor - Full Stepping

from time import sleep_ms
from machine import Pin

PA = Pin(16,Pin.OUT)
PB = Pin(17,Pin.OUT)
PC = Pin(18,Pin.OUT)
PD = Pin(19,Pin.OUT)

TABLE = [1, 2, 4, 8]

def Step(X):
    Y = TABLE[X % 4]
    PA.value( Y & 8 )
    PB.value( Y & 4 )
    PC.value( Y & 2 )
    PD.value( Y & 1 )
    
x = 0
for i in range(0,100):
    x += 1
    Step(x)
    sleep_ms(10)


# Half Stepping
# Stepper Motor - Half Stepping

from time import sleep_ms
from machine import Pin

PA = Pin(16,Pin.OUT)
PB = Pin(17,Pin.OUT)
PC = Pin(18,Pin.OUT)
PD = Pin(19,Pin.OUT)

TABLE = [1, 3, 2, 6, 4, 12, 8, 9]

def Step(X):
    Y = TABLE[X % 8]
    PA.value( Y & 8 )
    PB.value( Y & 4 )
    PC.value( Y & 2 )
    PD.value( Y & 1 )
    
x = 0
for i in range(0,200):
    x += 1
    Step(x)
    sleep_ms(10)


# Microstepping
# Micro-Stepping;  32 steps per cycle
from machine import Pin, PWM
from time import sleep_ms

PA = Pin(16,Pin.OUT)
PA = PWM(Pin(16))
PA.freq(100)
PA.duty_u16(0)

PB = Pin(17,Pin.OUT)
PB = PWM(Pin(17))
PB.freq(100)
PB.duty_u16(0)

PC = Pin(18,Pin.OUT)
PC = PWM(Pin(18))
PC.freq(100)
PC.duty_u16(0)

PD = Pin(19,Pin.OUT)
PD = PWM(Pin(19))
PD.freq(100)
PD.duty_u16(0)

TABLE32 = [0, 12681, 24874, 36112, 45962, 54046, 60052, 63751, 65000, 63751, 60052, 54046, 45962, 36112, 24874, 12681, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def Step32(X):
    A = TABLE32[X % 32]
    PA.duty_u16(A)
    B = TABLE32[(X+8) % 32]
    PB.duty_u16(B)
    C = TABLE32[(X+16) % 32]
    PC.duty_u16(C)
    D = TABLE32[(X+24) % 32]
    PD.duty_u16(D)
    
x = 0
for i in range(0,1600):
    x += 1
    Step32(x)
    sleep_ms(5)

PA.duty_u16(0)
PB.duty_u16(0)
PC.duty_u16(0)
PD.duty_u16(0)


# Digital Servo
from machine import Pin
from time import sleep_ms

# GP14 = push button (decrease angle)
# GP15 = push button (increae angle)
# GP16 = control input to digital servo motor

Up = Pin(15, Pin.IN, Pin.PULL_UP)
Down = Pin(14, Pin.IN, Pin.PULL_UP)

Control = Pin(16, Pin.OUT)
Control = PWM(Pin(16))
Control.freq(50)

x = 1_500_000

while(1):
    if(Up.value() == 0):
        x += 1000
    if(Down.value() == 0):
        x -= 1000
    if(x < 500_000):
        x = 500_000
    if(x > 2_500_000):
        x = 2_500_000
    Control.duty_ns(x)
    sleep_ms(1)