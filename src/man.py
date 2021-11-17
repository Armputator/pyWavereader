import re
import json
import os

def print_man(args):
    file = open(find_man(args)) #open file belonging to command given as parameter in args
    for line in file.readlines:
        print(line)

    file.close()

def find_man(args):
    files = [f for f in os.listdir('../man') if os.path.isfile(f)]  # list all files in directory pyWavereader/man 
    for d in dir:
        if len(re.findall(re.split("\-",args), d)) > 0:
            return d