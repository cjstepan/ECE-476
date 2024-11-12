from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
import LCD

# Initialize LCD
# Display 3 results on screen
# check if the new result is better than any of the previous attempts
# if so, replace that data with new data

result_1 = result_2 = result_3 = new_result = [0] * 200
distance = [125, 125, 125]
temp_distance = [0]
LCD.Init()
White = LCD.RGB(255,255,255)
Black = LCD.RGB(0,0,0)
Yellow = LCD.RGB(250,250,0)
LCD.Clear(Black)
LCD.Title('Top Jumps', White, Black)

LCD.Text2('First Place: ', 40, 50, Yellow, Black)
LCD.Text2('Second Place: ', 40, 100, Yellow, Black)
LCD.Text2('Third Place: ', 40, 150, Yellow, Black)

sleep_ms(500)
LCD.Text2(str(distance[0]) + ' cm ', 320, 50, White, Black)
LCD.Text2(str(distance[1]) + ' cm ', 320, 100, White, Black)
LCD.Text2(str(distance[2]) + ' cm ', 320, 150, White, Black)

for i in range(0,3):
    if temp_distance[i] > distance[i]:
        distance[i] = temp_distance[i]
