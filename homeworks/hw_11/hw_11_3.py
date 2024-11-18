from machine import Pin, I2C
from time import sleep
import network
import socket
import json
import gc
from neopixel import NeoPixel

# Hardware setup
np = NeoPixel(Pin(11), 8, bpp=3, timing=1)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
Beeper = Pin(13, Pin.OUT)
clear_tree_btn = Pin(1, Pin.IN, Pin.PULL_UP)
start_race_btn = Pin(15, Pin.IN, Pin.PULL_UP)
# Add shutdown button
shutdown_btn = Pin(14, Pin.IN, Pin.PULL_UP)  # Add a new pin for shutdown

class NetworkManager:
    def __init__(self, ssid='PicoStarterTree', password='racetime123'):
        self.ssid = ssid
        self.password = password
        self.ap = network.WLAN(network.AP_IF)
        self.active = False
        self.clients = set()
        
    def start(self):
        print("Starting Access Point...")
        self.ap.config(essid=self.ssid, password=self.password)
        self.ap.active(True)
        
        # Wait for AP to be active
        retry_count = 0
        while not self.ap.active() and retry_count < 10:
            print("Waiting for AP to start...")
            sleep(1)
            retry_count += 1
            
        if self.ap.active():
            self.active = True
            print('Access Point Active')
            print('Network config:', self.ap.ifconfig())
            return True
        else:
            print("Failed to start Access Point")
            return False
            
    def stop(self):
        print("Shutting down network...")
        # Close all client connections
        for client in self.clients.copy():
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Disable AP
        try:
            self.ap.active(False)
            self.active = False
            print("Network shutdown complete")
        except:
            print("Error during network shutdown")

class WebSocketServer:
    def __init__(self, network_manager):
        self.network_manager = network_manager
        self.socket = None
        self.running = False
        
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('', 80))
            self.socket.listen(5)
            self.socket.setblocking(False)  # Non-blocking socket
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.running = True
            print("WebSocket server started")
            return True
        except Exception as e:
            print("Failed to start WebSocket server:", e)
            return False
            
    def stop(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("WebSocket server stopped")

    def accept_new_connections(self):
        try:
            conn, addr = self.socket.accept()
            print(f"New connection from {addr}")
            conn.setblocking(False)
            request = conn.recv(1024).decode('utf-8')
            
            if 'GET / ' in request:
                conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'.encode() + html.encode())
                conn.close()
            elif 'Upgrade: websocket' in request:
                if handle_websocket_upgrade(conn):
                    self.network_manager.clients.add(conn)
                    print(f"WebSocket client connected. Total clients: {len(self.network_manager.clients)}")
        except:
            pass

def send_ws_update(network_manager, led_id, r, g, b):
    msg = json.dumps({'id': str(led_id), 'r': r, 'g': g, 'b': b})
    frame = bytearray([0x81, len(msg)]) + msg.encode()
    
    # Send to all clients, handle disconnections
    for client in network_manager.clients.copy():
        try:
            client.send(frame)
        except Exception as e:
            print(f"Client disconnected: {e}")
            try:
                client.close()
            except:
                pass
            network_manager.clients.remove(client)
            gc.collect()  # Clean up memory

def handle_websocket_frame(data):
    # Basic WebSocket frame decoding
    payload_len = data[1] & 127
    if payload_len == 126:
        mask_start = 4
    elif payload_len == 127:
        mask_start = 10
    else:
        mask_start = 2
    
    masks = data[mask_start:mask_start+4]
    payload_start = mask_start + 4
    payload = data[payload_start:]
    
    decoded = bytearray()
    for i in range(len(payload)):
        decoded.append(payload[i] ^ masks[i % 4])
    
    return decoded.decode('utf-8')

# Your existing HTML content here (unchanged)
html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous"
    />
    <style>
      .dot {
        height: 50px;
        width: 50px;
        border-radius: 50%;
        display: inline-block;
        margin: 5px;
      }
      body {
        text-align: center;
        padding: 20px;
      }
      .btn {
        margin: 10px;
      }
    </style>
    <title>Starter Tree Control</title>
  </head>
  <body>
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
      crossorigin="anonymous"
    ></script>
    <div id="dots">
      <span id="7" class="dot"></span><br />
      <span id="6" class="dot"></span><br />
      <span id="5" class="dot"></span><br />
      <span id="4" class="dot"></span><br />
      <span id="3" class="dot"></span><br />
      <span id="2" class="dot"></span><br />
      <span id="1" class="dot"></span><br />
      <span id="0" class="dot"></span><br />
    </div>
    <button onclick="clearTree()" id="clear_tree_btn" class="btn btn-secondary">Clear Start Tree</button>
    <button onclick="startRace()" id="start_race_btn" class="btn btn-success">Start Race</button>
    
    <script>
      let ws = new WebSocket('ws://' + window.location.hostname + ':80/ws');
      
      ws.onmessage = function(event) {
        let data = JSON.parse(event.data);
        let dot = document.getElementById(data.id);
        dot.style.backgroundColor = `rgb(${data.r},${data.g},${data.b})`;
      };
      
      function clearTree() {
        ws.send(JSON.stringify({action: 'clear'}));
      }
      
      function startRace() {
        ws.send(JSON.stringify({action: 'start'}));
      }
    </script>
  </body>
</html>'''  # Your existing HTML content

def main():
    # Initialize network and server
    network_manager = NetworkManager()
    if not network_manager.start():
        print("Failed to start network manager")
        return

    server = WebSocketServer(network_manager)
    if not server.start():
        network_manager.stop()
        print("Failed to start WebSocket server")
        return

    print("System startup complete")
    
    try:
        while True:
            # Check for shutdown request
            if shutdown_btn.value() == 0:
                print("Shutdown requested")
                break
                
            # Accept new connections
            if server.running:
                server.accept_new_connections()
            
            # Handle physical buttons (your existing logic)
            if clear_tree_btn.value() == 0:
                clear_strip(network_manager)
                print("Starter Tree Cleared")
                Beep()
                sleep(.1)
                Beep()
                
            if start_race_btn.value() == 0:
                start_race_sequence(network_manager)
            
            # Handle WebSocket messages from clients
            for client in network_manager.clients.copy():
                try:
                    data = client.recv(1024)
                    if data:
                        msg = json.loads(handle_websocket_frame(data))
                        if msg['action'] == 'clear':
                            clear_strip(network_manager)
                        elif msg['action'] == 'start':
                            start_race_sequence(network_manager)
                except:
                    continue
            
            sleep(0.01)  # Prevent CPU hogging
            gc.collect()  # Regular memory cleanup
            
    except Exception as e:
        print(f"Main loop error: {e}")
    finally:
        # Clean shutdown
        print("Starting clean shutdown...")
        clear_strip(network_manager)  # Turn off LEDs
        server.stop()
        network_manager.stop()
        gc.collect()
        print("Shutdown complete")

def clear_strip(network_manager):
    np.fill([0,0,0])
    np.write()
    # Update web clients
    for i in range(8):
        send_ws_update(network_manager, i, 0, 0, 0)

def start_race_sequence(network_manager):
    Beep()
    clear_strip(network_manager)
    for i in reversed(range(8)):
        rgb_value = int((1/(i+1))*125)
        np[i] = (rgb_value, rgb_value, 0)
        np.write()
        send_ws_update(network_manager, i, rgb_value, rgb_value, 0)
        sleep(1)
    
    np.fill([0,200,0])
    np.write()
    for i in range(8):
        send_ws_update(network_manager, i, 0, 200, 0)
    Beep()
    print("Race Started")

if __name__ == '__main__':
    main()