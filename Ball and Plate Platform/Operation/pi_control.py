'''! @file pi_control.py
This file contains the Position Control class
    
@author David Hefter, Mathew Smith, Akanksha Maddi, Amanda Westmoreland
@date   31-Oct-2023
@copyright (c) 2023 by Nobody and released under GNU Public License v3
'''
import utime
from encoder_reader import Encoder_Reader
from motor_driver import Motor_Driver

class PI_Control:
    """! 
    This class implements a closed loop position control for a motor
    """
    def __init__(self, Kp, Ki, Kd, setpoint, encoder, motor):
        """! 
        Creates a closed loop by initializing values
        used for closed loop control.
        @param Kp: gain for position
        @param Ki: gain for integral
        @param Kd: gain for derivative
        @param setpoint: sets the initial setpoint for the controller
        @param encoder: takes an encoder_reader class for the system
        @param motor: takes a motor_driver class for the system
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.pwm = 0
        self.pwm_P = 0
        self.pwm_I = 0
        self.pwm_D = 0
        self.total_error = 0
        self.setpoint = setpoint
        #self.values = [0, 0]
        self.encoder = encoder
        self.motor = motor
        self.time = utime.ticks_ms()
        self.prev_time = utime.ticks_ms()

    def run(self, setpoint):
        """! 
        Updates the system parameters
        @param setpoint: sets the setpoint for the controller
        """
        self.setpoint = setpoint
        #self.values[0] = utime.ticks_ms() - self.time
        #self.values[1] = self.encoder.read()
        
        if(utime.ticks_ms() - self.prev_time == 0):
            time = .001
        else:
            time = utime.ticks_ms() - self.prev_time
            
        sat = 99.9  # Saturation limit      
        self.total_error += (self.setpoint - self.encoder.read())
        
        self.pwm_P = self.Kp * (self.setpoint - self.encoder.read())
        if self.pwm_P > sat:
            self.pwm_P = sat
        elif self.pwm_P < -sat:
            self.pwm_P = -sat
        
        self.pwm_I = self.Ki * self.total_error
        if self.pwm_I > sat:
            self.pwm_P = sat
        elif self.pwm_I < -sat:
            self.pwm_I = -sat
        
        # pwm_D = Kd * error / time
        self.pwm_D = self.Kd * (self.setpoint - self.encoder.read()) / time
        if self.pwm_D > sat:
            self.pwm_D = sat
        elif self.pwm_D < -sat:
            self.pwm_D = -sat
        
        self.pwm = self.pwm_P + self.pwm_I + self.pwm_D
        if self.pwm > sat:
            self.pwm = sat
        elif self.pwm < -sat:
            self.pwm = -sat
        #self.motor.get_duty_cycle()
        self.prev_time = utime.ticks_ms()

    def reset_values(self):
        """! 
        Resets the system values and time
        """
        #self.values = [0, 0]
        self.time = utime.ticks_ms()

    def set_setpoint(self, setpoint):
        """!
        Sets a new setpoint
        @param setpoint: The new setpoint
        """
        self.setpoint = setpoint
    
    def set_Kp(self, Kp):
        """!
        Sets a new controller gain
        @param Kp: The new controller gain
        """
        self.Kp = Kp

    def set_Ki(self, Ki):
        """!
        Sets a new controller gain
        @param Ki: The new controller gain
        """
        self.Ki = Ki
        
    def set_Kd(self, Kd):
        """!
        Sets a new controller gain
        @param Kd: The new controller gain
        """
        self.Kd = Kd

    def print_values(self):
        """!
        Print the values collected from running
        """
        for i in range(0, len(self.values[0])):
            print(str(self.values[0][i]) + "," + str(self.values[1][i]))
        
    def get_pwm(self):
        """!
        Print the total pwm
        """
        print(self.pwm)
    
    def get_pwm_P(self):
        """!
        Print the protional pwm
        """
        print(self.pwm_P)
        
    def get_pwm_I(self):
        """!
        Print the integral pwm
        """
        print(self.pwm_I)
        
    def get_pwm_D(self):
        """!
        Print the differential  pwm
        """
        print(self.pwm_D)
        
# Run this test code when the file is run
if __name__ == "__main__":
    # Set up encoder pins
    en1_pin = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer3 = pyb.Timer(4, prescaler=0, period=0xFFFF)
    e = Encoder_Reader(en1_pin, en2_pin, timer3)
    
    # Set up motor for the B pins
    en_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    tim = pyb.Timer(3, prescaler = 0 , period = 0xFFFF)
    m = Motor_Driver(en_pin, in1pin, in2pin, tim)
    
    # Set up control class
    Kp = 0.05       # Motor control parameter
    Ki = 0.0
    Kd = 0.0
    freq = 1/.002
    c = PI_Control(Kp, Ki, Kd, freq, 0, e, m)
    
    time = utime.ticks_ms()
    itime = time
    # Get references to the share and queue which have been passed to this task
    degrees = 10
    scale = 2000
    print("// Run Forward")
    while utime.ticks_ms()- itime < 10000:
        utime.sleep_ms(2)
        c.run(degrees * scale)
        c.get_pwm()
    print("// Return to start")
    #while utime.ticks_ms() - itime < 20000:
    #    utime.sleep_ms(2)
    #    c.run(0)
    #    c.get_pwm()
    m.set_duty_cycle(0)
    print("// TEST COMPLETE //")