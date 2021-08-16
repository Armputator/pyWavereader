#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-09

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
import time
import csv

##def switch(arg):
##    case = 
##    if arg == 

#def interpreter(str):
    #if()
    
#def set_dev(var0):
    
def initt(port, baud = 9600, bytesize = 8, timeout = 5, stopbits = 1, parity = "even"):
    try:
        if stopbits == 0 or stopbits > 2:
            raise Exception("Error in function call initt(" + port + str(baud) + str(bytesize) + str(timeout) + str(stopbits) + str(parity) + ")\nArgument stopbits must be either 1 (one) or 2 (two)")
            
        else:
            ser = serial.Serial(port = port, baudrate = baud, bytesize = bytesize, timeout = timeout, stopbits = serial.STOPBITS_ONE if stopbits == 1 else serial.STOPBITS_TWO)
            return ser
    except:
        print("Exiting initt()")


def get_data(open_port,var0=None):
    try:
        if open_port.in_waiting > 0:
            
            open_port.flushInput()
            ser_data = open_port.readline()
            print(ser_data)

            #decoded_data = float(ser_data[0:len(ser_data)-2].decode("utf-8"))
            #print(decoded_data)

            with open("DSO138_data_" + str(time.time()) + ".csv","a") as f:
                writer = csv.writer(f,delimiter=", ")
                writer.writerow([time.time(), decoded_bytes])

    except:
        print("Exiting get_data()")
        

while True:
    myport = initt("COM7", 115200)
    try:
        get_data(myport)

    except:
        print("Keyboard interrupt")
        break
    ##x = raw_input("" + ">>: ")
