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

ser = serial.Serial('COM5')
ser.flushInput()

def get_data():
    try:
        ser_bytes = ser.readline()
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
        with open("DSO138_data_" + str(time.time()) + ".csv","a") as f:
            writer = csv.writer(f,delimiter=", ")
            writer.writerow([time.time(), decoded_bytes])

    except:
        print("Keyboard interrupt called")

while True:
    
        
