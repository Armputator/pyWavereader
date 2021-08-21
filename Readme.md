# pyWavereader
## Python based Waveform reader tool for the DSO138mini 1-channel oscilloscope

[![Build Status]]()
Last Revision: 2021-Aug-18

Written by D.Hainsch / Ampy 

pyWavereader is a small and simple tool, designed to optimize the workflow when working with the DSO138mini oscilloscope
Via a usb-ttl converter, such as the CH340 etc., the DSO138mini can transmit it's currently captured waveform via UART.
Factory settings are as follows:
- baudrate = 115200
- bytesize = 8
- parity = none
- stopbits = 1

pyWavereader has been developed on Windows 10, Microsoft Visual Studio Code to be executed on Python version 3.7.6 interpreter or higher.
During development it has been tested with the DSO138mini, running on Firmware 113-13816-111, connected to a CH340 usb-ttl converter on COM5

## **Features**


## **Commands**

Most commands take multiple arguments, but not multiple instances of the same option
Options must be introduced with a dash "-", predecessed by one or more whitespace(s)
Every option consists of one standard american alphabet letter
If an option can set a parameter, the argument must be appended to the option letter with an equal sign "=" and then the argument

EXAMPLE
: init i=myName p=COM1 r=9600

### Runtime Control

*exit - closes all ports and quits runtime*
SYNOPSIS
: exit

DESCRIPTION
: closes all ports in list all_ports before quitting python runtime, returns user to original terminal

takes no arguments

*help - returns man page for a given command*
SYNOPSIS
: help [COMMAND]

DESCRIPTION
: prints the man page about the command(s) given as argument or if -a option is given prints all possible commands

-a, prints all commands, function call ignores all other argument if this is given

EXAMPLES
: help -init
 help -a -init
 second function call will ignore the -init argument

### Serial Control

*init - initializes COM port as Interface during the current runtime*
SYNOPSIS
: init [OPTIONS]

DESCRIPTION
: initializes serial port with an interface name adressable by user

mandatory arguments are

-i=[INTERFACE]
-p=[PORT]
-r=[BAUDRATE]

optional arguments are
-b=[BYTESIZE], default value is 8 (eight)
-a=[PARITY], default is none
-s=[STOPBITS], default is 1 (one)

EXAMPLES
: init -i=MyPort -p=COM5 -r=115200

*close - closes interface*
SYNOPSIS
: close [INTERFACE] [PORT]

DESCRIPTION
: closes serial port via either port or interface name

first argument must either be interface name or port name following the -p option
-p=[PORT]

EXAMPLES
: close MyPort
  close -p=COM5

## **Installation**

## **Programming Interface**

## Development

## Building for source

## License
