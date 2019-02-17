#-*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import subprocess
import configparser
from time import sleep

from launchpad import Launchpad
from winkeyevent import PressKey, ReleaseKey

DEBUG = True

typeForActionDefine = {"0" : "KEYIN", "1" : "EXEC", "2" : "CODE", "3" : "WAVE", "9": "SPECIAL"}

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
    doloop = True
    while doloop:
        try:
            msg = lp.getMsg()
            if msg:
                key = str(msg['message'][0]) + str(msg['message'][1])
                try:
                    typeForAction, action = settings['action'][key].split(',')

                    if DEBUG is True:
                        print("key is in settings.ini")
                        print("type is {}, key is [{}], command is {}".format(typeForActionDefine[typeForAction], key, action))

                    #윈도우 키입력 신호 발생
                    if typeForActionDefine[typeForAction] == "KEYIN":
                        PressKey(int(action, 0))
                        ReleaseKey(int(action, 0))
                    #지정된 명령어 실행
                    elif typeForActionDefine[typeForAction] == "EXEC":
                        process = subprocess.Popen(action, creationflags=subprocess.DETACHED_PROCESS)
                    #계이름 연주?
                    elif typeForActionDefine[typeForAction] == "CODE":
                        pass
                    #음성파일 연주?
                    elif typeForActionDefine[typeForAction] == "WAVE":
                        pass
                    #현재 프로그램 기능으로 사용할 항목
                    elif typeForActionDefine[typeForAction] == "SPECIAL":
                        if key == "15336":
                            doloop = False
                            raise KeyboardInterrupt
                    else:
                        pass

                except KeyError as e:
                    if DEBUG is True:
                        print("key[{}] is not in settings.ini".format(key))
                        print(e)
            
                except ValueError as e:
                    if DEBUG is True:
                        print(e)
                        
                except OSError as e:
                    if DEBUG is True:
                        print(e)
            
        except KeyboardInterrupt as e:
            if DEBUG is True:
                print("user keyInterrupt")
                print(e)
            doloop = False

    lp.disconnect()
    sys.exit()        