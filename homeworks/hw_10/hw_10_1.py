from machine import UART, Pin
from time import sleep_ms
import LCD

# UART Init
uart0 = UART(0, 9600) # initialize with id=0
uart0.init(9600, bits=8, parity=None, stop=1, tx=0, rx=1) # tx/rx on pin 0/1

# Button and Beeper Init
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)
Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Beeper = Pin(13, Pin.OUT)

# LCD Init
White = LCD.RGB(255,255,255)
Black = LCD.RGB(0,0,0)
Orange = LCD.RGB(255,140,0)
Red = LCD.RGB(222,0,0)

LCD.Init()
LCD.Clear(Black)

# Global Flag
Error_Flag = 0
Record_Flag = 0
speed = [0]*3
knots_to_mph = 1.15078

def Beep():
    Beeper.value(1)
    sleep_ms(100)
    Beeper.value(0)

def Str2Num(X):
    global Error_Flag
    n = len(X)
    y = 0
    flag = 0
    k = 0
    for i in range(0,n):
        z = chr(ord(X[i:i+1]))
        if(z in {'0','1','2','3','4','5','6','7','8','9','0','.'}):
            if(z == '.'):
                flag = 1
            else:
                if(flag == 0):
                    y = 10*y + int(z)
                else:
                    k -= 1
                    y = y + int(z) * (10 ** k)
        else:
            Error_Flag = 1
    return(y)

def GPS_Read_Line():
    flag = 0
    msg = ''
    while(flag == 0):
        x = uart0.read(1)
        if(x != None):
            x = ord(x)
            if(chr(x) == '$'):
                msg = ''
            if(x == 13):
                flag = 1
            else:
                msg = msg + chr(x)
    return(msg)


def GPS_Read():
    flag = 0
    
    while(flag == 0):
        x = GPS_Read_Line()
        if(len(x) > 52):
            if(x[3] == 'R'): # $GPRMC
                flag = 1   
                time = Str2Num(x[7:16])
                lat = Str2Num(x[21:29])
                lon = Str2Num(x[35:43])
                speed = Str2Num(x[46:51])
    
    return([time, lat, lon, speed])

def get_max_speed_mph(file, current_index):
    f = open(file, "r")
    data = f.readlines()
    max_speed_mph = -1
    for i in range(current_index, len(data)):
        speed_mph = float(data[i])
        if speed_mph > max_speed_mph:
            max_speed_mph = speed_mph
    return max_speed_mph

LCD.Title('Top Speeds', White, Black)
LCD.Text2('First Place: ', 40, 50, Orange, Black)
LCD.Text2('Second Place: ', 40, 100, Orange, Black)
LCD.Text2('Third Place: ', 40, 150, Orange, Black)

while(Button14.value() == 1):
    Error_Flag = 1
    while(Error_Flag == 1):
        Error_Flag = 0
        [t, x, y, v] = GPS_Read()
    if(Button15.value() == 0):
        Record_Flag = not Record_Flag
        if(Record_Flag):
            Beep()
            f =  open("GPS_Speed.txt", "a")
            current_index = len(f.readlines())
            print('Recording')
            LCD.Text('Recording',5,5,Red,Black)
        else:
            Beep()
            sleep_ms(100)
            Beep()
            f.close()
            print('Recording Stopped')
            LCD.Text('         ',5,5,Red,Black)
            
            # parse the file to get the max speed for the recording and display it on the LCD Screen
            max_speed_mph = get_max_speed_mph("GPS_Speed.txt", current_index)
            speed.append(max_speed_mph) # add the velocity in mph to top speeds
            print(f"Max Speed = {max_speed_mph:.3f}")
            speed.sort(reverse=True) # sort the list to get the top 3 speeds
            print(f"List={speed[0]:.3f}, {speed[1]:.3f}, {speed[2]:.3f}")
            sleep_ms(50)
            LCD.Text2(f'{speed[0]:.3f} mph ', 320, 50, White, Black)
            LCD.Text2(f'{speed[1]:.3f} mph ', 320, 100, White, Black)
            LCD.Text2(f'{speed[2]:.3f} mph ', 320, 150, White, Black)
        while(Button15.value() == 0):
            pass
    if(Record_Flag):
        f.write(f'{(v * knots_to_mph):.3f}  \n')

for _ in range(0,3):
    Beep()  
    sleep_ms(100)
print("stop")
