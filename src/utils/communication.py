import serial

##Serial Port Init##
ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'   #DON'T  CHANGE
ser.timeout = 1
try:
    ser.open()
except:
    try:
        ser.port = 'COM3'   #CHANGE HERE
        ser.open()
    except:
        print("Cannot find Arduino")
        pass

def send_to_Arduino(data_to_send):
    ser.write(data_to_send)
    
def send_fi_to_Arduino(data, arm_num):
    try:
        if arm_num == 2:
            data = int(data)
        elif arm_num == 3:
            data = int(data) + 90
        if data < 0 :
            data = 0
        data_to_send = str(arm_num) + str(data) + '\n'
        send_to_Arduino(data_to_send.encode())
    except:
        "Cannot send data to Arduino!!"