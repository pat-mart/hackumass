import serial
import time
#initialize connection to arduino over serial port
def init_connection(port):
    try:
        s = serial.Serial(port,9600,timeout=1)
        time.sleep(2)
        print("port open::"+port)
        return s
    except:
        print("init connection failed")
        return None
#verify connection is ready and can be written
# def verify(s:serial.Serial):
#         if s==None:
#             print("verification failed")
#             return
#         data = "0\n"
#         s.write(data.encode(encoding='ascii'))
#         while s.in_waiting==0: pass
#         if s.in_waiting>0:
#            print(s.readline())
#         s.flush()
#write a single color to an index

#write a single color to a range of indices
def turnOn(serial:serial.Serial,index1,index2,r,g,b):
    try:
        data = "1 "+str(index1)+" "+str(index2)+" "+str(r)+" "+str(g)+" "+str(b)+"\n"
        serial.write(data.encode(encoding='ascii'))
    except:
        print("error in arduino write CMD:turnOn") 

#clear a range of values
def turnOff(serial:serial.Serial,index1,index2):
    try:
        data = "1 "+str(index1)+" "+str(index2)+" "+"0"+" "+"0"+" "+"0"+"\n"
        serial.write(data.encode(encoding='ascii'))
    except:
        print("error in arduino write CMD:turnOff")

#turn on sound based LED response
def soundModeOn(serial:serial.Serial, r, g, b):
    try:
        data = "2 "+str(r)+" "+str(g)+" "+str(b)+"\n"
        serial.write(data.encode(encoding='ascii'))
    except:
        print("error in arduino write CMD:soundModeOn")

def soundModeOff(serial:serial.Serial):
    try:
        data = "3 0 \n"
        serial.write(data.encode(encoding='ascii'))
    except:
        print("error in arduino write CMD:soundModeOff")  