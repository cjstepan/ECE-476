from machine import Pin
from time import sleep

# Define the pins for the LEDs
Led17 = Pin(17, Pin.OUT)
Led16 = Pin(16, Pin.OUT)

# Define the pins for the buttons
Button15 = Pin(15, Pin.IN)
Button14 = Pin(14, Pin.IN)

# Define the pins for the buzzer
Buzzer = Pin(13, Pin.OUT)

# 1. Write a Python program which turns on the LEDs based upon which buttons are pressed:
#       GP16: Turn on if both buttons are pressed (logic AND)
#       GP17: Turn on if only one button is pressed (logic XOR)

def btn_logic():
    while True:
        if Button14.value() == 1 and Button15.value() == 1:
            Led16.value(1)
            Led17.value(0)
        elif Button14.value() == 1 or Button15.value() == 1:
            Led16.value(0)
            Led17.value(1)
        else:
            Led16.value(0)
            Led17.value(0)
        sleep(0.1)

btn_logic()


# 2. Write a Python program which counts when you press the buttons
#       The counter starts at 0
#       When you press and release GP14, the counter increases by 1
#       When you press and release GP15, the counter increases by 10

def btn_count():
    count = 0
    while True:
        if Button14.value() == 1:
            count += 1
        elif Button15.value() == 1:
            count += 10
        print(count)
        sleep(0.1)

btn_count()


# == Combination Lock ==

# 3. Write a subroutine which generates a random number form 0 to 255

def random_number():
    

# 4. Write a subroutine which reads a 74165 shift register and returns a number from 0 to 255

# 5. Write a Python program which simulates a combination lock
#       Test your code
#       Display the actual code and your guess
#       Verify your code returns the correct messages (too high, too low, correct)

# 6. Demonstrate your code in a video