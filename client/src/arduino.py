import serial
#initialize connection to arduino over serial port
def init_connection(port):
    try:
        s = serial.Serial(port,9600,timeout=1)
        while s.is_open != True: pass
        print("port open::"+port)
        return s
    except:
        print("init connection failed")
        return None
#verify connection is ready and can be written
def verify(s:serial.Serial):
        if s==None:
            print("verification failed")
            return
        data = "0\n"
        s.write(data.encode(encoding='ascii'))
        while s.in_waiting==0: pass
        if s.in_waiting>0:
           print(s.readline())
        s.flush()
#write a single color to an index
def write1(serial:serial.Serial, index, r,g,b):
    try:   
        data = "1 "+str(index)+" "+str(r)+" "+str(g)+" "+str(b)+"\n"
        serial.write(data.encode(encoding='ascii'))
    except:
        print("error in arduino write CMD:1") 
#write a single color to a range of indices
def write2(serial:serial.Serial,index1,index2,r,g,b):
    try:
        data = "2 "+str(index1)+" "+str(index2)+" "+str(r)+" "+str(g)+" "+str(b)+"\n"
        serial.write(data.encode(encoding='ascii'))
    except:
        print("error in arduino write CMD:2") 