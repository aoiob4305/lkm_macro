#-*- coding:utf-8 -*-

import sys
import time
from rtmidi.midiutil import open_midiinput, open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON
from rtmidi import MidiIn, MidiOut

DEBUG = True

# novation lunchkeymini data from http://
row1 = (96, 97, 98, 99, 100, 101, 102, 103, 104)  # LED indices, first row
row2 = (112, 113, 114, 115, 116, 117, 118, 119, 120)  # LED incides, second row
leds = row1 + row2
control_mode_on = [NOTE_ON, 0x0C, 0x7F]
control_mode_off = [NOTE_ON, 0x0C, 0x00]

class Launchpad(object):
    def __init__(self):
        self.midiin = None
        self.midiout = None

    def __del__(self):
        if self.midiin is not None:
            self.midiin.close_port()
            self.midiin.cancel_callback()
        if self.midiout is not None:
            self.midiout.close_port()
    
    def connect(self, inport, outport):
        try:
            self.midiin, self.inport_name = open_midiinput(inport)
            self.midiout, self.outport_name = open_midioutput(outport)
            return True

        except OSError:
            print("there is no midi device")
            sys.exit()
            return False

        except (EOFError, KeyboardInterrupt):
            sys.exit()
            return False

    def disconnect(self):
        try:
            self.midiin.close_port()
            self.midiin.cancel_callback()
            self.midiout.close_port()
            return True

        except (EOFError, KeyboardInterrupt):
            sys.exit()
            return False

    def getDeviceList(self):
        midiin = MidiIn()
        midiout = MidiOut()
        try:
            return (midiin.get_ports(), midiout.get_ports())
        except Exception as e:
            if DEBUG == True:
                print(e)
            return False

    def getMsg(self):
        try:
            timer = time.time()
            msg = self.midiin.get_message()
            if msg:
                message, deltatime = msg
                timer += deltatime

                if DEBUG == True:
                    print("[%s] @%0.6f %r" % (self.inport_name, timer, message))

                return {"name": self.inport_name, "timer": timer, "message": message}

            time.sleep(0.01)
            return False

        except KeyboardInterrupt:
            self.__del__()
    
    def playNote(self, note, vel, timeval):
        try:
            self.midiout.send_message([NOTE_ON, note, vel])
            time.sleep(timeval)
            self.midiout.send_message([NOTE_OFF, note, 0])
            return True
        except Exception as e:
            print(e)
            return False

    def writeLed(self, led_id, color_vel):
        self.midiout.send_message(control_mode_on)
        time.sleep(2)
        self.midiout.send_message([NOTE_ON, led_id, color_vel])
        time.sleep(2)
        self.midiout.send_message(control_mode_off)
        return True