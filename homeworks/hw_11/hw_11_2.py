from machine import Pin, I2C
from time import sleep
from neopixel import NeoPixel
import network
import socket

np = NeoPixel(Pin(11), 8, bpp=3, timing=1)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
Beeper = Pin(13, Pin.OUT)
clear_tree_btn = Pin(14, Pin.IN, Pin.PULL_UP)
start_race_btn = Pin(15, Pin.IN, Pin.PULL_UP)

ssid = 'Pico-Network'
password = 'PASSWORD'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
    pass
print('AP Mode Is Active, You can Now Connect')
print('IP Address To Connect to:: ' + ap.ifconfig()[0])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

def web_page():
    f = open("starter_tree.html","rt")
    x = f.readlines()
    for i in range(len(x)):
        led_line = x[i].find("span id=")
        if not led_line == -1:
            x[i].replace("rgb(187, 187, 187)", "rgb({})")
        
    x = x.replace('\r\n',' ')
    return(x)

def clear_strip():
    np.fill([0,0,0])
    np.write()

def Beep():
    Beeper.value(1)
    sleep(.1)
    Beeper.value(0)

def clear_tree():
    clear_strip()
    print("Starter Tree Cleared")
    Beep()
    sleep(.1)
    Beep()

def start_race():
    Beep()
    clear_strip()
    for i in reversed(range(8)):
        rgb_value = int((1/(i+1))*125)
        print(rgb_value, i)
        np.__setitem__(i, [rgb_value,rgb_value,0])
        np.write()
        sleep(1)
    np.fill([0,200,0])
    np.write()
    Beep()
    print("Race Started")

clear_strip()
clear_tree_btn.irq(trigger=Pin.IRQ_FALLING, handler=clear_tree)
start_race_btn.irq(trigger=Pin.IRQ_FALLING, handler=start_race)
while(1):
    conn, addr = s.accept()
    print('conn = ', conn)
    print('addr = ', addr)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    conn.close()
