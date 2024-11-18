# https://www.youtube.com/watch?v=cZNoXXIEPbg
## https://medium.com/@shilleh/creating-a-wireless-network-with-raspberry-pi-pico-w-part-1-c896211f2bd6

import network
import time
import socket

def web_page():
    f = open("32_HelloWorld.html","rt")
    x = f.read()
    x = x.replace('\r\n',' ')
    return(x)

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


