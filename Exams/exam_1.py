from machine import Pin, PWM
from time import sleep_ms
import random
import math

led = Pin(17, Pin.OUT)
led_pwm = PWM(led)
light_off = Pin(0, Pin.IN)
light_on_1 = Pin(1, Pin.IN)
light_on_10 = Pin(2, Pin.IN)
light_on_100 = Pin(3, Pin.IN)
led_pwm.freq(100)

while True:
    if light_off.value() == 1:
        led_pwm.duty_u16(0)
    if light_on_1.value() == 1:
        led_pwm.duty_u16(655) # 1%
    if light_on_10.value() == 1:
        led_pwm.duty_u16(6555) # 10%
    if light_on_100.value() == 1:
        led_pwm.duty_u16(65546) # 100%
    sleep_ms(100)

# Question 2

food_2_btn = Pin(14, Pin.IN, Pin.PULL_UP)
food_3_btn = Pin(15, Pin.IN, Pin.PULL_UP)
food_count = 0

while(1):
    if(food_2_btn.value() == 0):
        food_count += 2
    elif(food_3_btn.value() == 0):
        food_count += 3
    if random.randint(0,10) == 2: # 10% chance for food to be taken away
        sleep_ms(1000)
        food_count -= 2
    print(f'Food Count: {food_count}')
    sleep_ms(100)


# Question 4
def Voltage(T):
    R = 3000*math.exp((4000/(T+273)) - (4000/298))
    R_a = ((1/R) + (1/10000))**-1
    R_b = R_a + 5000
    V = (R_b/(R_b + 3000))*3.3
    return V
