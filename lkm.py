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

lp = Launchpad()
result = lp.connect(midiInPort, midiOutPort)

if result is True:
    while True:
        msg = lp.getMsg()
        if msg:
            key = str(msg['message'][0]) + str(msg['message'][1])
            try:
                command = settings['command'][key]
                subprocess.Popen(command, creationflags=subprocess.DETACHED_PROCESS)
                print("key is in settings.ini")
                print("command is {}".format(command))
            except KeyError:
                print("key is not in settings.ini")
            
            except KeyboardInterrupt:
                lp.disconnect()
                sys.exit()
        
