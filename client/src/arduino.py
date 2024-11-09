import serial as serial

def init_connection(port):
    return serial.Serial(port,9600,timeout=1)

def verify(serial):
    try:
        serial.write("0")
        while serial.inWaiting==0: pass
        if serial.inWaiting>0:
           print(serial.read())
        serial.flush
    except:
        print("connection failed")

def write(serial, index, rgb):
    try:   
        serial.write("1"+str(index)+str(rgb))
        serial.flush()
    except:
        print("error in arduino write CMD:1") 


def write(serial,index1,index2,rgb):
    try:   
        serial.write("2"+str(index1)+str(index2)+str(rgb))
        serial.flush()
    except:
        print("error in arduino write CMD:2") 