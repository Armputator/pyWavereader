#written on python version 3.7.6
#written by Ampy
#last revision: 2021-Aug-09



class device():

    def __init__(self, name, port, baud = 9600, bytesize = 8, timeout = 5, stopbits = 1, parity = 'none', lines = 1):
        self.name = name
        self._port = port
        self._baudrate = baud
        self._bytesize = bytesize
        self._timeout = timeout
        self._stopbits = stopbits
        self._parity = parity
        self._lines = lines

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baud):
        if baud > 0:
            self._baudrate = baud
        else:
            raise Exception("Error: Baudrate cannot be 0 or lower")
    

All_Devices = {"DSO138mini" : device("DSO138mini", 'COM5', 115200, lines = 1024+17),}


