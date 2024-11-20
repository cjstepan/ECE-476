import netman, socket, network, time
from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(11), 8, bpp=3, timing=1)
Beeper = Pin(13, Pin.OUT)

ssid = 'Taco Bell-Guest' 
password = 'thestepans'
country = 'US'

race_flag = 0
N = 7

# disconnect if already connected
wlan = network.WLAN(network.STA_IF)
if(wlan.active()):
    wlan.active(0)
    wlan.disconnect()
    time.sleep(1)
    
wifi_connection = netman.connectWiFi(ssid,password,country)
IP_Address = wifi_connection[0]

def web_page(ip_address):
    global race_flag, N
    f = open("starter_tree.html")
    led_array = []
    if race_flag:
        if N >= 0 and N <= 7 :
            if N == 7:
                Beep()
                clear_strip()
            np.__setitem__(N, [225,225,0])
            np.write()
            N -= 1
        elif N <= 0:
            np.fill([0,200,0])
            np.write()
            Beep()
            N = 100
    for i in range(8):
        led_array.append(np.__getitem__(i))
        
    x = f.read()
    x = x.replace('\r\n',' ')
    x = x.replace('aaaaa',ip_address)
    x = x.replace("id='0' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[0][0]}, {led_array[0][1]}, 0)'")
    x = x.replace("id='1' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[1][0]}, {led_array[1][1]}, 0)'")
    x = x.replace("id='2' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[2][0]}, {led_array[2][1]}, 0)'")
    x = x.replace("id='3' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[3][0]}, {led_array[3][1]}, 0)'")
    x = x.replace("id='4' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[4][0]}, {led_array[4][1]}, 0)'")
    x = x.replace("id='5' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[5][0]}, {led_array[5][1]}, 0)'")
    x = x.replace("id='6' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[6][0]}, {led_array[6][1]}, 0)'")
    x = x.replace("id='7' style='background-color: rgb(187, 187, 187)'", f"id='0' style='background-color: rgb({led_array[7][0]}, {led_array[7][1]}, 0)'")
    return(x)

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
wlan = socket.socket()
wlan.bind(addr)
wlan.listen(1)

print('listening on', addr)

def clear_strip():
    np.fill([0,0,0])
    np.write()

def Beep():
    Beeper.value(1)
    time.sleep(.1)
    Beeper.value(0)

def clear_tree():
    global race_flag, N
    clear_strip()
    print("Starter Tree Cleared")
    Beep()
    time.sleep(.1)
    Beep()
    race_flag = 0
    N = 7

def start_race():
    global race_flag, N
    race_flag = 1
    N = 7
    

last_request = "None"
while(1):
    flag = 0
    while(flag == 0):
        conn, addr = wlan.accept()
        request = conn.recv(1024)
        request = request.decode('utf-8')
        if(request.find('favicon') > 0):
            flag = 1
        else:
            response = web_page(IP_Address)
            conn.send(response)
            conn.close()

    n = request.find('Referer:')+9
    request = request[n:]
    n = request.find('\r\n')
    request = request[0:n]
    for i in range(0,10):
        n = request.find('/')+1
        if(n>0):
            request = request[n:]
    print(request)
    if(request == 'start_race' and not last_request == 'start_race'):
        start_race()
        last_request = 'start_race'
    if(request == 'clear_tree' and not last_request == 'clear_tree'):
        clear_tree()
        last_request = 'clear_tree'
    response = web_page(IP_Address)
    conn.send(response)
    conn.close()
