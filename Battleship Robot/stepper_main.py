# -*- coding: utf-8 -*-
'''!    @file stepper_main.py
        @brief                                  A class designed to test implementation of the stepper driver
                                                
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
                                                
        @date                                   November 14, 2022
'''
import Stepper_Driver
from pyb import Timer, Pin

if __name__ == '__main__':
    timer_channel = 2
    timer = Timer(8, freq = 20000000)
    CLKpin = Pin.cpu.C7
    SPInum = 2
    CSpin1 = Pin.cpu.C3
    CSmode1 = Pin.OUT_PP
    CSvalue1 = 1
    ENpin1 = Pin.cpu.C4
    CSpin2 = Pin.cpu.C2
    CSmode2 = Pin.OUT_PP
    CSvalue2 = 1
    ENpin2 = Pin.cpu.C0
    
    a = Stepper_Driver.Stepper_Driver(timer_channel, timer, CLKpin, SPInum, CSpin1, CSmode1, CSvalue1, CSpin2, CSmode2, CSvalue2, ENpin1, ENpin2)