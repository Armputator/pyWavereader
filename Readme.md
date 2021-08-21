# pyWavereader
## Python based Waveform reader tool for the DSO138mini 1-channel oscilloscope

[![Build Status]]()
Last Revision: 2021-Aug-21

Written by D.Hainsch / Ampy 

pyWavereader is a small and simple tool, designed to optimize the workflow when working with the DSO138mini oscilloscope
Via a usb-ttl converter, such as the CH340 etc., the DSO138mini can transmit it's currently captured waveform via UART.
Factory settings are as follows:
- baudrate = 115200
- bytesize = 8
- parity = none
- stopbits = 1

pyWavereader has been developed on Windows 10, Microsoft Visual Studio Code to be executed on Python version 3.7.6 interpreter or higher.
During development it has been tested with the DSO138mini, running on Firmware 113-13816-111, connected to a CH340 usb-ttl converter on COM5.
As such most standard settings will be optimized for this setup.

## **Features**
- Initalize serial ports and manage them as user friendly interfaces
- Read serial data
- Save serial data to timestamped csv files
- Plot serial data via mathplotlib (future update)

## **Commands**

Most commands take multiple arguments, but not multiple instances of the same option
Options must be introduced with a dash "-", predecessed by one or more whitespace(s)
Every option consists of one standard american alphabet letter
If an option takes an argument, the argument must be appended to the option letter with an equal sign "=" inbetween

EXAMPLE
: `init -i=myName -p=COM1 -r=9600`
---
---
### Runtime Control

*leave - closes all ports and quits runtime*

SYNOPSIS
: leave

DESCRIPTION
: closes all ports in list all_ports before quitting python runtime, returns user to original terminal
takes no arguments

EXAMPLES
: leave
---
*help - returns man page for a given command*

SYNOPSIS
: help [COMMAND]

DESCRIPTION
: prints the man page about the command(s) given as argument or if -a option is given prints all possible commands
`-a`, prints all commands, function call ignores all other argument if this is given

EXAMPLES
: `help -init`
 `help -a`, this call will ignore the -init argument

### Serial Control

*init - initializes COM port as Interface during the current runtime*

SYNOPSIS
: init [OPTIONS]

DESCRIPTION
: initializes serial port with an interface name adressable by user
adds entry for how many lines must be read when reading from this com port
mandatory arguments are

-i=[INTERFACE]
-p=[PORT]
-r=[BAUDRATE]
-l=[LINES]

optional arguments are
-b=[BYTESIZE], default value is 8 (eight)
-a=[PARITY], default is none
-s=[STOPBITS], default is 1 (one)

EXAMPLES 
: `init -i=MyPort -p=COM5 -r=115200 -l=1041 (STANDARD FOR DSO138mini)`
---
*close - closes interface*

SYNOPSIS
: close -i=[INTERFACE]

DESCRIPTION
: closes serial port via interface name

EXAMPLES
: `close -i=MyPort`
---
*set_port - sets interface as current working port*

SYNOPSIS
: set_port -i=[INTERFACE]

DESCRIPTION
: Sets serial port assigned to interface name as current communication port. becomes standard for all Serial Communication Commands
Also sets the lines value for read operation

EXAMPLES
: `set_port -i=MyPort`
---
*show_ports - shows currently detectable ports*

SYNOPSIS
: show_ports [OPTIONS]

DESCRIPTION
: shows ports detectable by runtime

-p, shows all ports connected to system
-i, shows all interfaces
-c, shows all initilized ports as saved in all_ports list
-m, shows current standard port

EXAMPLES
: `show_ports -p `
---
---
### Serial Communication

*get_data - reads n number of lines from a previously initialized serial port*

SYNOPSIS
: get_data [OPTIONS]

DESCRIPTION
: reads n amount of lines from a serial port. Standard serial port is the empty default port, with default line value of 1 (one).
If set_port has been called, get_data reads from the new standard interface with the selected amount of lines. If no amount of lines is assigned to interface, reads default 1 (one) line


-i=[INTERFACE]
-l=[LINES], including the argument will override the line value assigned to i or current standard port

EXAMPLES
: `get_data, reads from current standard port`
`get_data -i=MyPort, reads 1041 lines from MyPort (see init examples)`
`get_data -i=MyPort -l=2, reads 2 lines from MyPort`
---
---
### Data Commands

*save_data - saves data to csv file* Still in building

SYNOPSIS
: save_data

DESCRIPTION
: Saves serial data in a csv file in the included savedata folder. Filename built from timestamp and Device name (Currently only DO138mini,  future support for more devices in planning)
Takes no arguments

EXAMPLES
: `save_data`
---
---
## **Installation**
Python version 3.7.6 or higher is required
Extract contents and start the runtime via 
`python src/wavereader.py`

## Programming Interface

## Contribute
If you have any Suggestions or would like to add or improve, feel free to branch and start pull requests. As of right now, i feel most comfortable approving any changes to master myself but i am open to change!

## Building for source

## License
