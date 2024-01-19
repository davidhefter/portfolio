"""! @encoder_class.py
This file contains code definitions for encoder behavior. 

@author David Hefter, Mathew Smith, Akanksha Maddi, Amanda Westmoreland
@date   31-Oct-2023
@copyright (c) 2023 by Nobody and released under GNU Public License v3
"""
import time
import pyb
    
class Encoder_Reader:
    """!
    This class contains code for reading the encoder
    """
    def __init__(self, tim, cha_pin, chb_pin, inter_tim_chan, inter_tim_freq):
        """!
        This class contains code for reading the encoder

        @param tim: Timer channel for encoder
        param cha_pin: Encoder channel A pin
        @param chb_pint: Encoder channel B pin
        @param inter_tim_chan: Timer channel for interrupts
        @param inter_tim_freq: Frequency for timer interrupts
        """
        self.cha_pin = cha_pin
        self.chb_pin = chb_pin
        self.tim = tim
        self.inter_tim = pyb.Timer(inter_tim_chan, freq=inter_tim_freq, callback=self.handleflow)
        
        self.ch1B = self.tim.channel(1, pyb.Timer.ENC_AB, pin=cha_pin)
        self.ch2B = self.tim.channel(2, pyb.Timer.ENC_AB, pin=chb_pin)
        
        self.old_pos = self.tim.counter()
        self.cur_pos = self.old_pos
        self.en_readout = 0
        self.delta = 0
        self.inter_tim.callback(self.handleflow)

        
        self.zero()
    
    def handleflow(self, tim):
        """!
        @details: this function controls the response of overflow or underflow on the encoder
        starts count over after 1 full rotation
        recognizes when the encoder moves backwards
        """
        self.old_pos = self.cur_pos
        self.cur_pos = self.tim.counter()
        self.delta = self.cur_pos - self.old_pos
        if self.delta > 32767:
            self.delta -= 65536
        elif self.delta < -32768:
            self.delta += 65536
        self.en_readout += self.delta
    
    def read(self):
        """!
        @details: this function returns the new posistion of the encoder based on
        its previous position
        """
        self.handleflow(self.inter_tim)
        return self.en_readout

    def zero(self):
        """!
        @details: this function zeros the encoder value, resetting it to 0
        """
        self.cur_pos = self.tim.counter()
        self.old_pos = self.cur_pos
        self.en_readout = 0

    
    

if __name__ == "__main__":
    """en1_pin = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer4 = pyb.Timer(4, prescaler=0, period=0xFFFF) 
    reader = Encoder_Reader(en1_pin, en2_pin, timer4)
    while True: 
        print(reader.read())
        time.sleep(0.1)"""

