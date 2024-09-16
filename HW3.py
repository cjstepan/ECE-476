from machine import Pin, SPI
from time import sleep, sleep_us
import random

# Define Inputs (Push Buttons)
btn_14 = Pin(14, Pin.IN)
btn_15 = Pin(15, Pin.IN)

# Define Outputs (LEDs, Beeper)
LATCH = Pin(9, Pin.OUT)
beeper = Pin(13, Pin.OUT)
led_16 = Pin(16, Pin.OUT)
led_17 = Pin(17, Pin.OUT)

# Define SPI
spi = SPI(1, baudrate=10_000, polarity=0, phase=0, bits=8, sck=10, mosi=11, miso=12)

# 1. Write a Python program which turns on the LEDs based upon which buttons are pressed:
#       GP16: Turn on if both buttons are pressed (logic AND)
#       GP17: Turn on if only one button is pressed (logic XOR)
def btn_logic():
    while True:
        if btn_14.value() == 0 and btn_15.value() == 0:
            led_16.on()
            led_17.off()
        elif btn_14.value() == 0 or btn_15.value() == 0:
            led_16.off()
            led_17.on()
        else:
            led_16.off()
            led_17.off()
        sleep(0.1)

# btn_logic()


# 2. Write a Python program which counts when you press the buttons
#       The counter starts at 0
#       When you press and release GP14, the counter increases by 1
#       When you press and release GP15, the counter increases by 10
def btn_count():
    count = 0
    prev_btn_14 = btn_14.value()
    prev_btn_15 = btn_15.value()

    while True:
        curr_btn_14 = btn_14.value()
        curr_btn_15 = btn_15.value()

        if prev_btn_14 == 1 and curr_btn_14 == 0:
            count += 1
            print(count)
        elif prev_btn_15 == 1 and curr_btn_15 == 0:
            count += 10
            print(count)

        prev_btn_14 = curr_btn_14
        prev_btn_15 = curr_btn_15

        sleep(0.1)

# btn_count()

# == Combination Lock ==
# Write a program where you guess the value of an 8-bit binary number, defined by a 74165 shift register
# -At the start of the game, the Pico picks a random number from 0 to 255 and the LED GP16 is turned off
# -You then set the eight binary inputs to the shift register
# -Once set, press GP15
# -It then tells you if your guess was too low, too high, or correct
# -If the guess is correct, turn on the LED on GP16

# 3. Write a subroutine which generates a random number from 0 to 255
def get_rand():
    return random.randint(0, 255)

for _ in range(0,10):
    print(f'rand={get_rand()}')

# 4. Write a subroutine which reads a 74165 shift register and returns a number from 0 to 255
def LS165_read():
    LATCH.value(1)
    sleep_us(10)
    LATCH.value(0)
    sleep_us(10)
    LATCH.value(1)
    # data is latched - now shift it in
    rxdata = spi.read(1, 0x42)
    return(rxdata)

# while(1):
#     Y = LS165_read()
#     print(Y)
#     sleep(0.1)

# 5. Write a Python program which simulates a combination lock
#       Test your code
#       Display the actual code and your guess
#       Verify your code returns the correct messages (too high, too low, correct)

def combination_lock():
    code = get_rand()
    print(f'Code: {code}')

    while True:
        guess = input('Enter your guess: ')
        print(f'Guess: {guess}')
        
        if guess < code:
            print('Too Low')
        elif guess > code:
            print('Too High')
        else:
            print('Correct')
            break

# 6. Demonstrate your code in a video

# Questions for Glower:
# 4. Am I supposed to use get_rand to generate my random number, load it into the shift register, and then read it back?
# -For the homework, generate the random number as the code, and then read the shift register to get the guess
# -The shift register guess is set by the user with lines tied low and high
# -Verify the shift register output by reading it back on an oscilloscope
# What does testing code look like? I got docked on HW2 for not testing
# -Test each subroutine multiple times, that should suffice
# 5. for simulating the combo lock, do I need to continually guess until I get the combo right, or just once?
# -continually guess until it's right

# Shift Register pinout:
# Connect Clk to Oscilloscope (shift on rising edge, read bit on falling edge)
# Pin 9/Q_H - Output (connect to oscilloscope with clk to verify read out)
# Pin 15/CLK INH - Clk inhibit should be tied high
# Tie all other pins randomly to 3.3V or GND to determine the guess