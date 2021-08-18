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
import man
import re
import serial
import serial.tools.list_ports as port_list
import time
import csv
#---------------------------------------------------GLOBAL VARIABLES---------------------------------------------------#

all_ports = list()
all_interfaces = dict()
myPort = serial.Serial()
min_lines = 0
startup = False
decoded_list = list()

#---------------------------------------------------CLASSES---------------------------------------------------#


#---------------------------------------------------FUNCTIONS---------------------------------------------------#

def exit():
    myPort.close()
    exit()

#empty dict declaration because i am getting annoyed at vscode syntax parsing saying it doesnt recognise
base_cmnds = dict()
def input_interpreter(input):
    cmdstr = re.split("\s+\-", input)

    return base_cmnds[(cmdstr[0])](cmdstr[1::])

def _init(args):
    print("Hooray!")
    if args[0] == "-help":
        print(man._init())
    #return serial.Serial(port = port, baudrate = baud, bytesize = bytesize, timeout = timeout, stopbits = serial.STOPBITS_ONE if stopbits == 1 else serial.STOPBITS_TWO)
    myPort.port = re.findall("-p",args)
    myPort.baudrate = re.findall("-r",args)
    #myPort.bytes = 
    if myPort.is_open == False:
        myPort.open()

def load(args): #NOT FINISHED
    return _init()

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


def get_data():
        print("Waiting for data")
        for i in range(min_lines):
            myPort_data = myPort.readline()
            decoded_data = myPort_data.decode("Ascii")

            decoded_list.append(decoded_data)
            #print(decoded_data)


def save_data():
        with open("DSO138_data_" + str(time.time()) + ".csv","a") as target_file:
            for line in decoded_list:        
                writer = csv.writer(target_file,delimiter=' ')
                writer.writerow(line)
        
#---------------------------------------------------COMMANDS_DICTIONARY---------------------------------------------------#

cmnd_interpreter = {
    'init' : _init, 
    'show_ports' : show_ports,
    'get_data' : get_data, 
    'close' : close,
    'exit' : exit,
    'save' : save_data,
    }

base_cmnds = cmnd_interpreter
#---------------------------------------------------RUNTIME---------------------------------------------------#

if False:
    myPort = serial.Serial('COM5', 115200)
    for i in range(1024+17):
        myPort_data = myPort.readline()
        print(myPort_data.decode("Ascii"))

while True:
    if startup == False:
        #init('COM5', 115200)
        #myPort.port = 'COM5'
        #myPort.baudrate = 115200
        #myPort.open()
        startup = True
    
    min_lines = 1024+17

    try:
        command = input( str(myPort.port) + " >$ ")
        cmnd_interpreter[command]()

    except:
        print("Keyboard interrupt")
        break
    
