# Question 1
def GPS_Problem(X):
    red = "\033[91m"
    if(X[4] == 'G'): # $GPGGA
        altitude = X[54:59]
        bstr = ' '.join(format(ord(c), '08b') for c in altitude)
        return red + bstr
    return(b'')

test_string = "$GPGGA,205246.00,4649.55240,N,09652.11367,W,1,07,1.17,283.7,M,-27.5,M,,*69\r\n"

print(GPS_Problem(test_string))

# Question 2
def wifi_problem(x):
    str_match = 'N0=Hello+World&N1=3.14159'
    if x[21:46] == str_match:
        return {1, str_match}
    return {2, ''}

test_string = 'GET /action_page.php?N0=Hello+World&N1=3.14159'

print(wifi_problem("Hello World"))


# Question 3
test_msg = 'aa,bbbbb.bb/r/n'

X = [0] * 100
def BlueTooth_Problem(msg):
    global X
    mem_location_index = int(msg[0:2])
    stored_num = float(msg[3:11])
    X[mem_location_index] = stored_num
    print(mem_location_index, stored_num, X[mem_location_index])

BlueTooth_Problem('13,12345.67')

# Question 4
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

def stoplight_control(np_reg, neopixel):
    red = [50,0,0]
    yellow = [50,50,0]
    green = [0,50,0]
    black = [0,0,0]
    
    if np_reg[0] == 0:
        while True:
            neopixel.__setitem__(2,black)
            neopixel.__setitem__(1,black)
            neopixel.__setitem__(0,green)
            neopixel.write()
            sleep_ms(np_reg[1])
            neopixel.__setitem__(2,black)
            neopixel.__setitem__(1,yellow)
            neopixel.__setitem__(0,black)
            neopixel.write()
            sleep_ms(np_reg[2])
            neopixel.__setitem__(2,red)
            neopixel.__setitem__(1,black)
            neopixel.__setitem__(0,black)
            neopixel.write()
            sleep_ms(np_reg[3])

    elif np_reg[0] == 1:
        neopixel.fill([50,0,0])
        neopixel.write()