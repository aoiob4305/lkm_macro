#-*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import subprocess
import configparser
from time import sleep

from launchpad import Launchpad

settings = configparser.ConfigParser()
settings.read("settings.ini")

midiInPort = settings['midi']['midiInPort']
midiOutPort = settings['midi']['midiOutPort']
print("inport is {}, outport is {}".format(midiInPort, midiOutPort))

lp = Launchpad()
lp.getDeviceList()
result = lp.connect(midiInPort, midiOutPort)

if result is True:
    while True:
        msg = lp.getMsg()
        if msg:
            key = str(msg['message'][0]) + str(msg['message'][1])
            try:
                typeForAction, action = settings['command'][key].split(',')
                #subprocess.Popen(action, creationflags=subprocess.DETACHED_PROCESS)
                print("key is in settings.ini")
                print("type is {}, command is {}".format(typeForAction, action))
            except KeyError:
                print("key is not in settings.ini")
            
            except KeyboardInterrupt:
                lp.disconnect()
                sys.exit()
        
