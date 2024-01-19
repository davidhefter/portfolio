"""! @motor_driver.py
    This file contains a motor driver for senior project motors. 
    
    @author David Hefter, Mathew Smith, Akanksha Maddi, Amanda Westmoreland
    @date   31-Oct-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""

import pyb
class Motor_Driver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, timer, PWM_pin, DIR_pin, nSLP_pin, nFLT_pin, CS_pin, CS_ADc_pin, PWM_channel):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param timer: Timer for the Motor
        @param PWM_pin: PWM Pin for the Motor
        @param DIR_pin: Direction Pin for the Motor
        @param nSLP_pin: notSleep Pin for the Motor
        @param nFLT_pin: notFault Pin for the Motor
        @param CS_pin: Current Sensor Pin for the Motor
        @param CS_ADc_pin: Current Sensor Analog Digital Converter Pin for the Motor
        @param PWM_channel: Timer PWM Channel for the Motor
        """
        self.PWM_pin = PWM_pin
        self.DIR_pin = DIR_pin
        self.nSLP_pin = nSLP_pin
        self.nFLT_pin = nFLT_pin
        self.CS_pin = CS_pin
        self.CS_ADc_pin = CS_ADc_pin
        self.PWM_channel = PWM_channel
        self.pwm_return=0
        print ("Creating a motor driver")

    def enable (self):
        """!
        This method sets the enable pin to high, enabling the motor.
        """
        self.nSLP_pin.high()
    
    def disable (self):
        """!
        This method sets the enable pin to low, disabling the motor.
        """
        self.nSLP_pin.low()

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        if(level > 0):
            self.DIR_pin.high()
            self.PWM_channel.pulse_width_percent(level)
            self.pwm_return = level
        elif(level < 0):
            self.DIR_pin.low()
            self.PWM_channel.pulse_width_percent(level*-1)
            self.pwm_return = -level
        else:
            self.PWM_channel.pulse_width_percent(0)
            self.pwm_return = 0
    
    def get_duty_cycle(self):
        """!
        This method returns the duty cycle that the motor is currently set to.
        """
        print(self.pwm_return)
    
if __name__ == "__main__":
    pass
    """en_pin = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    tim = pyb.Timer(5, prescaler = 0 , period = 0xFFFF)
    moe = Motor_Driver(en_pin, in1pin, in2pin, tim)
    moe.set_duty_cycle(90)"""
