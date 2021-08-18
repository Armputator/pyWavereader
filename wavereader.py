#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-17

#Writing to Serial Port in Powershell

#PS> [System.IO.Ports.SerialPort]::getportnames()
#PS> $port= new-Object System.IO.Ports.SerialPort COM3,9600,None,8,one
#PS> $port.open()
#PS> $port.WriteLine("Hello world")
#PS> $port.Close()

#Reading from a Serial Port in Powershell

#PS> $port= new-Object System.IO.Ports.SerialPort COM3,9600,None,8,one
#PS> $port.Open()
#PS> $port.ReadLine()

import api
import serial
import serial.tools.list_ports as port_list
import time
import csv
#---------------------------------------------------GLOBAL VARIABLES---------------------------------------------------#

myPort = serial.Serial()
min_lines = 0
startup = False

#---------------------------------------------------CLASSES---------------------------------------------------#


#---------------------------------------------------FUNCTIONS---------------------------------------------------#
    
def init(port, baud = 9600, bytesize = 8, timeout = 5, stopbits = 1, parity = 'none'):

        ports = list(port_list.comports())
        i = 0
        found = False
        for p in ports:
            i+=1    
            print( str(i) + " >> " + str(p)[0:4])

            if str(p)[0:4] == port:
                print("COM Port found! Opening port " + port)
                found = True
                break

        if True:
            #return serial.Serial(port = port, baudrate = baud, bytesize = bytesize, timeout = timeout, stopbits = serial.STOPBITS_ONE if stopbits == 1 else serial.STOPBITS_TWO)
            myPort.baudrate = baud
            myPort.port = port
            if myPort.is_open == False:
                myPort.open()
            return

        raise Exception("COM Port " + port + " not available. Call show_ports() to see full list of ports")    


def close(port):
    try:
        if myPort.port == port and myPort.is_open == True:
            myPort.close()
        else:
            raise Exception("Target Port is not the current open port")

    except:
        print("Exiting close()")


def show_ports():
    ports = list(port_list.comports())
    for p in ports:
        print(p)

def exit():
    myPort.close()
    exit()

def get_data():
        decoded_list = []
        print("Waiting for data")
        for i in range(min_lines):
            myPort_data = myPort.readline()
            decoded_data = myPort_data.decode("Ascii")

            decoded_list.append(decoded_data)
            #print(decoded_data)

        with open("DSO138_data_" + str(time.time()) + ".csv","a") as target_file:
            for line in decoded_list:        
                writer = csv.writer(target_file,delimiter=' ')
                writer.writerow(line)
        
#---------------------------------------------------COMMANDS_DICTIONARY---------------------------------------------------#

cmnd_interpreter = {
    'show ports' : show_ports,
    'get data' : get_data, 
    'close' : close,
    'exit' : exit,
    }

#---------------------------------------------------RUNTIME---------------------------------------------------#

if False:
    myPort = serial.Serial('COM5', 115200)
    for i in range(1024+17):
        myPort_data = myPort.readline()
        print(myPort_data.decode("Ascii"))

while True:
    if startup == False:
        #init('COM5', 115200)
        myPort.port = 'COM5'
        myPort.baudrate = 115200
        myPort.open()
        #myPort = serial.Serial('COM5', 115200)
        startup = True
    
    min_lines = 1024+17

    try:
        command = input( str(myPort.port) + " >$ ")
        cmnd_interpreter[command]()

    except:
        print("Keyboard interrupt")
        break
    
