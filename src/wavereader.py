#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-20

import re
import serial
import serial.tools.list_ports as port_list
import time
import csv
import json

#---------------------------------------------------GLOBAL VARIABLES---------------------------------------------------#

all_ports = list()  #List of all ports
all_interfaces = dict() #Dictionary connecting Interface names as String to respective entry in all_ports
myPort = serial.Serial() #empty default port
min_lines = 1 #default amount of minimum lines
startup = False #variable for runtime starting process
raw_list = list() #lsit for saving raw serial data
decoded_list = list() #list for saving serial data

#---------------------------------------------------CLASSES---------------------------------------------------#


#---------------------------------------------------FUNCTIONS---------------------------------------------------#

def exit(args):
    for p in all_ports:
        p.close()
    exit()

#empty dict declaration because i am getting annoyed at vscode syntax parsing saying it doesnt recognise
base_cmnds = dict()
def input_interpreter(input):
    cmdstr = re.split("\s+\-", input)

    for c in cmdstr:
        for d in cmdstr:
            if c[0:2] == d[0:2]:
                raise Exception("Cannot have multiple instances of the same option")
    
    return base_cmnds[(cmdstr[0])](cmdstr[1::])

def _init(args):
    
    if args[0] == "-help":
        print("placeholder for man page")
    #return serial.Serial(port = port, baudrate = baud, bytesize = bytesize, timeout = timeout, stopbits = serial.STOPBITS_ONE if stopbits == 1 else serial.STOPBITS_TWO)
    all_ports.append(serial.Serial(port = str((re.findall("-p=",args))[2::]), baudrate = int((re.findall("-r=",args))[2::])))
    all_interfaces[str((re.findall("-i=",args))[2::])] = all_ports[-1]
    
    #myPort.port = str((re.findall("-p",args))[2::])
    #myPort.baudrate = int((re.findall("-r",args))[2::])
    
    #if myPort.is_open == False:
    #    myPort.open()

def load(args): #NOT FINISHED
    return _init()

def close(interface):
    try:
        all_interfaces[interface]

    except:
        print("Exiting close()")


def show_ports(args):
    if re.findall("-p", args):
        ports = list(port_list.comports())
        for p in ports:
            print(p)
        
    if re.findall("-c", args):
        for i in all_interfaces.keys:
            print( ("Open" if str((all_interfaces[i]).is_open()) else "Closed") +  " >> " + str(i))


def get_data(args):
        lines = 0
        #print("Waiting for data")
        if re.findall("-l=",args):
            lines = ((re.findall("-l=",args))[0])[3::]
        else:
            lines = min_lines

        for i in range(lines):
            myPort_data = myPort.readline()
            raw_list.append(myPort_data)

        for i in range(lines):
            decoded_data = myPort_data.decode("Ascii")
            decoded_list.append(decoded_data)
            #print(decoded_data)
    

def save_data(args):
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
    
