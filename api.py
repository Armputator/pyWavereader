#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-09

class device:
    name = ""
    serial_type = ""


    def __init__(self, name, serial_type):
        self.name = name
        self.serial_type = serial_type

DSO138 = device("DSO138","8N1")

