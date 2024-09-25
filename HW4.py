from machine import ADC, Pin, PWM
from time import sleep_ms

Up = Pin(15, Pin.IN, Pin.PULL_UP)
Down = Pin(14, Pin.IN, Pin.PULL_DOWN)

Motor = Pin(17, Pin.OUT)
Motor = PWM(Pin(17))
Motor.freq(100)

Spkr = PWM(Pin(18))
Spkr.init(freq=100, duty_ns=5000)
Spkr.duty_u16(32768)

# Write a Python program to turn your Pico board into an electronic trombone
# -When the analog input (joystick) is all the way left, the Pico outputs 220Hz
# -When the analog input is all the way right, the Pico outputs 440Hz
# -The frequency is proportional to the voltage inbetween
# -When button GP14 is pressed, output a square wave with the frequency determined by the joystick
# position
# -When released, no sound is output
# 1) Give the resulting Python program
def trombone():
    But_14 = Pin(14, Pin.IN, Pin.PULL_DOWN)
    a2d0 = ADC(0)
    a2d1 = ADC(1)
    k = 3.3 / 65535

    Max_freq = 440
    Min_freq = 220
    def calculate_ticks_to_freq(ticks):
        return int((ticks /65535)*(Max_freq-Min_freq) + Min_freq)

    count = 2000
    while(count > 0):
        if not Down.value():
            Spkr.duty_u16(32768)
            a0 = a2d0.read_u16()
            a1 = a2d1.read_u16()
            V0 = a0 * k
            V1 = a1 * k
            print(calculate_ticks_to_freq(a0))
            Spkr.freq(calculate_ticks_to_freq(a0))
            sleep_ms(200)
            count -= 1
        else:
            try:
                Spkr.duty_u16(0)
            except:
                pass
    
    pwm.deinit()

# trombone()

# 2) Test your code at
#   -220Hz (analog input = 0V)
#   -440Hz (analog input = 3.3V)
#   -inbetween (check the voltage and frequency)
# 3) Demonstrate your electronic trombone


# Write a Python program so that a digital servo motor points at the sun (or some other light source)
# 4) Design hardware so that the voltage is a maximum (0-3.3V) when pointing at a light source
# --See attached photo of transistor as a switch circuit--
# 5) Write a Python subroutine to read the voltage from problem #4
def read_voltage():
    a2d0 = ADC(0)
    k = 3.3 / 4000
    sense_in = 0

    while(1):
        sense_in = k * (a2d0.read_u16() >> 4)
        sleep_ms(200)

# read_voltage()

# Check that the number returned is a maximum when pointing at the light source)
# 6) Write a Python subroutine which controls the angle of a DC servo motor
def control_servo():
    max_duty = 17000
    min_duty = 1000
    x = int((max_duty + min_duty) / 2)
    dx = 100

    a2d0 = ADC(2)
    k = 3.3 / 4000

    turn_left = False
    turn_right = True
    last_sense_in = 0
    sense_in = 0
    Status = "Searching"

    while(1):
        Motor.duty_u16(x)
        
        if turn_left:
            x += dx
            if x >= max_duty:
                x = max_duty
                turn_left = not turn_left
                turn_right = not turn_right
        elif turn_right:
            x -= dx
            if x <= min_duty:
                x = min_duty
                turn_left = not turn_left
                turn_right = not turn_right
        
        last_sense_in = sense_in
        sense_in = k * (a2d0.read_u16() >> 4)
        
        if sense_in > 2.5:
            turn_left = False
            turn_right = False
            Status = "Found Light"
        else:
            if sense_in+0.3 < last_sense_in:
               turn_left = not turn_left
               turn_right = not turn_right
               Status = "Searching"
            if not turn_left and not turn_right:
                turn_right = True
        sleep_ms(10)
        print(f'Left: {turn_left}    Right: {turn_right}   Status: {Status}    Sensor Read: {round(sense_in,2)} V    Motor Position: {x}')

# control_servo()
# Check that you can control the angle of the servo
# 7) Write a Python program that searches for what angle maximizes the output of the light sensor
# 8) Demonstrate your program