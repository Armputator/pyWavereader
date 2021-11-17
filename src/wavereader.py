#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-21

import re
import serial
from serial.serialutil import STOPBITS_ONE
import serial.tools.list_ports as port_list
import time
import csv
import json
import matplotlib
import man as manlib

#---------------------------------------------------GLOBAL VARIABLES---------------------------------------------------#

myPort = serial.Serial()    #empty default port
all_ports = list()      #List of all ports
all_interfaces = {"myPort" : myPort}    #Dictionary connecting Interface names as String to respective entry in all_ports
line_interface = {"myPort" : 1} #Dictionary connecting Interface names to line counts

min_lines = 1   #default amount of minimum lines
startup = False     #variable for runtime starting process

raw_list = list()   #list for saving raw serial data
decoded_list = list()   #list for saving serial data

last_file = None    #last file which was created

#---------------------------------------------------CLASSES---------------------------------------------------#

#---------------------------------------------------FUNCTIONS---------------------------------------------------#

    #---------------------------------------------------RUNTIME CONTROL---------------------------------------------------#
#empty dict declaration because i am getting annoyed at vscode syntax parsing saying it doesnt recognise
base_cmnds = dict()

def input_interpreter(input):
    cmdlist = re.split("\s+\-", input) ##separates command from options, treats multiple whitespaces as one#if an option argument and its equal sign is separated from option letter by whitespaces it will be misinterpreted
    options = str()
    #print("dissected input= ") #debug
    #print(cmdlist) #debug
    for c in cmdlist[1::]:
        options += '-' + c + ' '
    #print("extracted options= " + options) #debug

    for c in cmdlist:
        if len(re.findall(c[0:3:],options)) > 2:
            raise Exception("Cannot have multiple instances of the same option" + str(re.findall(c,options)))
    
    if cmdlist[0] == "leave":
        leave()
    else:
        try:
            return (base_cmnds[(cmdlist[0])])(options) #calls command and gives options as single string with each option seperated with one whitespace
        except:
            print("Command " + str(cmdlist[0]) + " could not be found")

def leave(args=None):
    for p in all_ports:
        if p.is_open == True:
            p.close()
    quit()

def man(args):  #can be called manually, call via help is preferred
    return manlib.print_man(args)


def help(args):
    if re.findall("\-a",args):
        for b in base_cmnds.keys():
            print(b) #print from base_cmnds

    else:
        man(args) #print man page of command
    

#---------------------------------------------------SERIAL CONTROL---------------------------------------------------#

def _init(args):
    #template
    #return serial.Serial(port = port, baudrate = baud, bytesize = bytesize, timeout = timeout, stopbits = serial.STOPBITS_ONE if stopbits == 1 else serial.STOPBITS_TWO)
    
    #print(((re.findall("\-r=\S*",args)))) #debug
    all_ports.append( 
        serial.Serial( 
            port = str(((re.findall("\-p=\S+",args))[0])[3::]),
            baudrate = int(((re.findall("\-r=\S+",args))[0])[3::]),
            #bytesize = (re.findall("\-b=\S*", args)[0])[3::] if re.findall("\-b=\S*", args) else 8,
            #timeout = int((re.findall("\-t=\S*", args)[0])[3::]) if re.findall("\-t=\S*", args) else 1,
        )
    )

    if re.findall("\s+\-l=\S+",args):
        line_interface[(re.findall("\-i=\S+",args)[0])[3::]] = int((re.findall("\-l=\S+",args)[0])[3::])
    
    #print((re.findall("\-i=\S*",args))[3::]) #debug
    all_interfaces[(re.findall("\-i=\S+",args)[0])[3::]] = all_ports[-1] #append interfaces list with interface name and assigned serial port
    

def load(args): #NOT FINISHED
    return _init()


def set_port(args):
    if re.findall("\-i=\S+",args):
       all_interfaces["myPort"] = all_interfaces[ ((re.findall("\-i=\S+",args))[0])[3::] ]
       line_interface["myPort"] = line_interface[ ((re.findall("\-i=\S+",args))[0])[3::] ]
    else:
        raise Exception("No port or inteface was given. Please name a Serial connection to set as default")


def close(args=None):
    for p in re.findall("\s+\-"):
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
    
    if re.findall("\-j",args):
        for p in all_ports:
            print(p)

    if re.findall("\-c",args):
        print(all_interfaces["myPort"])

#---------------------------------------------------SERIAL COMMUNICATION---------------------------------------------------#

def get_data(args):
    #print("Waiting for data")
    raw_list.clear()
    decoded_list.clear()
    lines = 0

    if re.findall("\-i=\S+",args):
        tempport = all_interfaces[ (re.findall("\-i=\S+",args)[0])[3::] ]
        lines = line_interface[ (re.findall("\-i=\S+",args)[0])[3::] ]
    else:
        tempport = all_interfaces["myPort"]
        lines = line_interface["myPort"]

    if re.findall("\-l=\S+",args):
        lines = int(((re.findall("\-l=\S+",args))[0])[3::])

    print("Waiting to read " + str(lines) + " lines!")

    for i in range(lines):
        _data = tempport.readline()
        raw_list.append(_data)

    for i in raw_list:
        decoded_data = i.decode("Ascii")
        print(decoded_data[0:-1:])
        decoded_list.append(decoded_data[0:-1:])
            
    #print(decoded_list)

#---------------------------------------------------DATA COMMANDS---------------------------------------------------#    

def save_data(args=None):
        last_file = "savedata\\DSO138_data_" + str(time.time()) + ".csv"
        with open(last_file,"a") as target_file:
            for line in decoded_list:
                #writer = csv.writer(target_file,delimiter=' ',doublequote= '|',quotechar='"',lineterminator=' ',skipinitialspace = True)
                #writer.writerow(line)
                #writer.writerow("".join(line))
                target_file.write(line)


def plot_data(args=None):
    try:
        if re.findall("\-f=\S+", args):
            with open((re.findall("\-f=\S+", args)[0])[3::],"r") as data_file:
                data = csv.reader(data_file,delimiter=' ',doublequote= '|',quotechar='"',lineterminator=' ',skipinitialspace = True)
                for row in data:
                    print("".join(row))

        elif last_file is not None:
            with open(last_file,"r") as data_file:
                data = csv.reader(data_file,delimiter=' ',doublequote= '|',quotechar='"',lineterminator=' ',skipinitialspace = True)
                for row in data:
                    print("".join(row))
        
        else:
            print("No file was previously created")
            return
    
    except:
        print("Error ocurred trying to open a data file with following arguments:\n->" + args + "<-")
        

#---------------------------------------------------COMMANDS_DICTIONARY---------------------------------------------------#

cmnd_dict = {
    'close' : close,
    'exit' : exit,
    'get_data' : get_data, 
    'help' : help,
    'init' : _init, 
    'load' : load,
    'man' : manlib.print_man,
    'plot_data' : plot_data,
    'set_port' : set_port,
    'show_ports' : show_ports,
    'save_data' : save_data,
    }

base_cmnds = cmnd_dict
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
