from machine import Pin, PWM

Spkr = Pin(18, Pin.OUT)
Spkr = PWM(Pin(18), freq=100, duty_u16=32768)
while(1):
    print(Spkr.freq())
