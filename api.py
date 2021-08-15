#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-09


class device:
    name = ""
    serial_type = ""
    previous = None
    next = None

    def __init__(self, name, serial_type):
        self.name = name
        self.serial_type = serial_type


All_Devices = {"DSO138mini" : device("DSO138mini", "8N1"),}

def setcurrent(name):
    return All_Devices[name]