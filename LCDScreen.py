import time,sys
import smbus
import RPi.GPIO as GPIO

        
class LCDScreen:

    DISPLAY_RGB_ADDR = 0x62
    DISPLAY_TEXT_ADDR = 0x3e

    def __init__(self):
        self.bus = smbus.SMBus(1)

    def textCommand(self,cmd):
        self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x80,cmd)

    def setText(self,text):
        self.textCommand(0x01) # clear display
        time.sleep(.05)
        self.textCommand(0x08 | 0x04) # display on, no cursor
        self.textCommand(0x28) # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x40,ord(c))

    