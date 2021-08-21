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

myPort = serial.Serial() #empty default port
all_ports = list()  #List of all ports
all_interfaces = {"myPort" : myPort} #Dictionary connecting Interface names as String to respective entry in all_ports

min_lines = 1 #default amount of minimum lines
startup = False #variable for runtime starting process

raw_list = list() #lsit for saving raw serial data
decoded_list = list() #list for saving serial data

#---------------------------------------------------CLASSES---------------------------------------------------#


#---------------------------------------------------FUNCTIONS---------------------------------------------------#

    #---------------------------------------------------RUNTIME CONTROL---------------------------------------------------#
def exit(args = None):
    for p in all_ports:
        if p.is_open == True:
            p.close()
    quit()

#empty dict declaration because i am getting annoyed at vscode syntax parsing saying it doesnt recognise
base_cmnds = dict()

def help(args):
    if re.findall("\-a",args):
        for b in base_cmnds.keys():
            print(b) #print from base_cmnds
    else:
        for a in args[:-1:]:
            print("no man pages available yet") #print man page of command
    

def input_interpreter(input):
    cmdlist = re.split("\s+\-", input) ##separates command from options, treats multiple whitespaces as one#if a option argument and its equal sign is separated from otion letter by whitespaces it will be misinterpreted
    options = str()
    print("dissected input= ")
    print(cmdlist)
    for c in cmdlist[1::]:
        options += '-' + c + ' '
    print("extracted options= " + options)

    for c in cmdlist:
        if len(re.findall(c[0:3:],options)) > 2:
            raise Exception("Cannot have multiple instances of the same option" + str(re.findall(c,options)))
    
    return (base_cmnds[(cmdlist[0])])(options) #calls command and gives options as single string with each option seperated with one whitespace

    #---------------------------------------------------SERIAL CONTROL---------------------------------------------------#

def _init(args):
    
    #return serial.Serial(port = port, baudrate = baud, bytesize = bytesize, timeout = timeout, stopbits = serial.STOPBITS_ONE if stopbits == 1 else serial.STOPBITS_TWO)
    
    #print(((re.findall("\-r=\S*",args)))) #debug
    all_ports.append( serial.Serial( port = str(((re.findall("\-p=\S*",args))[0])[3::]) , baudrate = int(((re.findall("\-r=\S*",args))[0])[3::]) ) )
    
    #print((re.findall("\-i=\S*",args))[3::]) #debug
    all_interfaces[(re.findall("\-i=\S*",args)[0])[3::]] = all_ports[-1] #append interfaces list with interface name and assigned serial port
    

def load(args): #NOT FINISHED
    return _init()


def set_port(args):
    if re.findall("\-i=\S*",args):
       all_interfaces["myPort"] = all_interfaces[ ((re.findall("\-i=\S*",args))[0])[3::] ]
    else:
        raise Exception("No port or inteface was given. Please name a Serial connection to set as default")


def close(args=None):
    for p in re.findall("\s+"):
        if all_interfaces[p].is_open:
            all_interfaces[p].close()

def show_ports(args):
    if re.findall("\-p", args):
        ports = list(port_list.comports())
        for p in ports:
            print(p)
        
    if re.findall("\-i", args):
        for i in all_interfaces.keys():
            print( ("Open" if str((all_interfaces[i]).is_open) else "Closed") +  " >> " + str(i))
    
    if re.findall("\-c",args):
        for p in all_ports:
            print(p)

    if re.findall("\-m",args):
        print(all_interfaces["myPort"])


def get_data(args):
        lines = 0
        #print("Waiting for data")
        if re.findall("l=",args):
            lines = ((re.findall("l=",args))[0])[3::]
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
    'exit' : exit,
    'init' : _init, 
    'help' : help,
    'load' : load,
    'set_port' : set_port,
    'close' : close,
    'show_ports' : show_ports,
    'get_data' : get_data, 
    'save_data' : save_data,
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
    
    #min_lines = 1024+17

    command = input(" >$ ")
    input_interpreter(command)

while False:
    try:
        #command = input( str(myPort.port) + " >$ ")
        command = input(" >$ ")
        input_interpreter(command)

    except:

        command = input( "Error encountered! Continue? [y/n]\n" )
        if command == "n":
            print("Exiting runtime")
            break
        elif command == "y":
            continue
        else:
            print("Keyboard interrupt")
            break
