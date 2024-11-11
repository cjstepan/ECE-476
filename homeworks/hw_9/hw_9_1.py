from machine import Pin, I2C
import time
import LCD

def reg_write(i2c, addr, reg, data):
    msg = bytearray()
    msg.append(data)
    i2c.writeto_mem(addr, reg, msg)
    
def reg_read(i2c, addr, reg, nbytes=1):
    if nbytes < 1:
        return bytearray()
    data = i2c.readfrom_mem(addr, reg, nbytes)
    return data

def accel_read(reg):
    x = reg_read(i2c, addr, reg, 2)
    y = (x[0] << 8) + x[1]
    if(y > 0x8000):
        y = y - 0x10000
    y = y / 0x8000
    return(y)

i2c = I2C(0, scl=Pin(1), sda=Pin(0))

Beeper = Pin(13, Pin.OUT)
Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)

def Beep():
    Beeper.value(1)
    time.sleep(0.1)
    Beeper.value(0)


# Print out any addresses found
devices = i2c.scan()
if devices:
    for d in devices:
        print('I2C Device Found:',hex(d))

addr = devices[0]
print('Communicating with ', hex(addr))

# set bandwidth
reg_write(i2c, 0x68, 0x1a, 5) # 10Hz
# set range
reg_write(i2c, 0x68, 0x1c, 0x00) # +/- 2g
RANGE = 2
# set clock freq
reg_write(i2c, 0x68, 0x6b, 0) # Internal 8MHz Clock

time.sleep(1)

LCD.Init()
Navy = LCD.RGB(0,0,5)
LCD.Clear(Navy)

npt = 200
Data = [ [0]*npt, [0]*npt, [0]*npt ]
t = [0]*npt

FileName = 'GY521_Jump.txt'

while(1):
    flag = 0
    while(Button14.value() == 1):
        if(Button15.value() == 0):
            if(flag == 0):
                print('Saving Data')
                f = open(FileName, "a")
                f.write('-----------------\n')
                for i in range(0,npt):
                    mx = str('{: 11.5f}'.format(Data[0][i]))
                    my = str('{: 11.5f}'.format(Data[1][i]))
                    mz = str('{: 11.5f}'.format(Data[2][i]))
                    f.write(mx + my + mz + '\n')
                f.close()
                flag = 1
        pass
    Beep()
    for i in range(0,npt):
        x = accel_read(0x3b) * RANGE
        y = accel_read(0x3d) * RANGE
        z = accel_read(0x3f) * RANGE
        Data[0][i] = x
        Data[1][i] = y
        Data[2][i] = z
        t[i] = i
        time.sleep(0.01)
    Data[0][0] = -RANGE
    Data[0][1] = +RANGE
    LCD.Clear(Navy)
    LCD.Plot(t,Data)
    for i in range(0,npt):
        print(Data[0][i], Data[1][i], Data[2][i])


if(0):
    for i in range(0,100):
        x = accel_read(0x3b) * RANGE
        y = accel_read(0x3d) * RANGE
        z = accel_read(0x3f) * RANGE

        mx = 'x" = ' + str('{: 5.3f}'.format(x))
        my = '    y" = ' + str('{: 5.3f}'.format(y))
        mz = '    z" = ' + str('{: 5.3f}'.format(z))

        print(x, y, z)
        #print(mx + my + mz, "   ",end="\r")
        time.sleep(0.1)

# Work on Displaying top 3 results on graphics display

# calculate distance as d = 1/8 at^2 where a=9.8m/s and t is the time aloft