#-*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import subprocess
import configparser
from time import sleep

from launchpad import Launchpad

DEBUG = True

settings = configparser.ConfigParser()
settings.read("settings.ini")

midiInPort = settings['midi']['midiInPort']
midiOutPort = settings['midi']['midiOutPort']

lp = Launchpad()

if DEBUG is True:
    il, ol = lp.getDeviceList()
    print("now available input is {}".format(il))
    print("now available output is {}".format(ol))
    print("inport is {}, outport is {}".format(midiInPort, midiOutPort))

result = lp.connect(midiInPort, midiOutPort)

if result is True:
    while True:
        msg = lp.getMsg()
        if msg:
            key = str(msg['message'][0]) + str(msg['message'][1])
            try:
                typeForAction, action = settings['command'][key].split(',')
                #subprocess.Popen(action, creationflags=subprocess.DETACHED_PROCESS)
                if DEBUG is True:
                    print("key is in settings.ini")
                    print("type is {}, command is {}".format(typeForAction, action))
            except KeyError:
                if DEBUG is True:
                    print("key[{}] is not in settings.ini".format(key))
            
            except KeyboardInterrupt:
                lp.disconnect()
                sys.exit()
        
