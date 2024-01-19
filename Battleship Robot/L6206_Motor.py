'''!    @file L6206_Motor.py
        @brief                                  Motor driver for L6206 motor. 
                                        
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
        @date                                   September 27, 2022
'''

'''!@file L6206.py
'''
from pyb import Pin, Timer
import time,pyb

class L6206_Motor:
    '''!@brief      A driver class for one channel of the L6206.
    @details    Objects of this lass can be used to apply PWM to a given
                DC motor on one channel of the L6206 from ST Microelectronics.
    '''

    def __init__ (self, PWM_tim, IN1_pin, IN2_pin, EN_pin, timer_CH1, timer_CH2):
        '''!@brief     Initializes and returns an object associated with a DC motor.
        '''
        self.PWM_time_ch1 = PWM_tim.channel(timer_CH1, Timer.PWM, pin = IN1_pin)
        self.PWM_time_ch2 = PWM_tim.channel(timer_CH2, Timer.PWM, pin = IN2_pin)
        self.EN_pin = Pin(EN_pin, mode = Pin.OUT_PP)
    
    
    def set_duty (self, duty):
        '''!@brief      Set the PWM duty cycle for the DC motor.
        @details    This method sets the duty cycle to be sent
                    to the L6206 to a given level. Positive values
                    cause effort in one direction, negative values
                    in the opposite direction.
        @param      duty A signed number holding the duty
                    cycle of the PWM signal sent to the L6206
        '''
        if duty>=0 and duty<=100:
            self.PWM_time_ch1.pulse_width_percent(100)
            self.PWM_time_ch2.pulse_width_percent(100-duty)
        elif duty<0 and duty>= -100:
            self.PWM_time_ch2.pulse_width_percent(100)
            self.PWM_time_ch1.pulse_width_percent(100+duty)      
        elif duty>100:
            self.PWM_time_ch1.pulse_width_percent(100)
            self.PWM_time_ch2.pulse_width_percent(0)
        elif duty<-100:
            self.PWM_time_ch2.pulse_width_percent(100)
            self.PWM_time_ch1.pulse_width_percent(0)
    
    
    def enable (self):
        '''!@brief      Enable one channel of the L6206.
        @details    This method sets the enable pin associated with one
                    channel of the L6206 high in order to enable that
                    channel of the motor driver.
        '''
        self.EN_pin.high()
    
    def disable (self):
        '''!@brief      Disable one channel of the L6206.
        @details    This method sets the enable pin associated with one
                    channel of the L6206 low in order to enable that
                    channel of the motor driver.
        '''
        self.EN_pin.low()

def fire(A,B,C):
    test = True
    st = time.ticks_ms()
    C.set_duty(100)
#    while test:
#        if time.ticks_ms() > st+1000:
#            C.set_duty(0)
#            A.set_duty(100)
#            B.set_duty(100)
#        if time.ticks_ms() > st+3000:
#            C.set_duty(-100)
#        if time.ticks_ms() > st+4000:
#            A.set_duty(0)
#            B.set_duty(0)
#            test=False
    while test:
        if time.ticks_ms() > st+750:
            C.set_duty(-100)
        if time.ticks_ms() > st+1000:
            C.set_duty(0)
        if time.ticks_ms() > st+3000:
            C.set_duty(-100)
        if time.ticks_ms() > st+3250:
            C.set_duty(0)
            test=False
    
    
        
if __name__ == '__main__':
    # Adjust the following code to write a test program for your L6206 class. Any
    # code within the if __name__ == '__main__' block will only run when the
    # script is executed as a standalone program. If the script is imported as
    # a module the code block will not run.
    
    # Create a timer object to use for motor control
    #tim_A = Timer(4, freq = 20_000)
    #tim_B = Timer(5, freq = 20_000)
    
    # Create an L6206 driver object. You will need to modify the code to facilitate
    # passing in the pins and timer objects needed to run the motors.
    #mot_A = L6206_Motor(tim_A, Pin.cpu.B6, Pin.cpu.B7, Pin.cpu.A10, 1, 2)
    #mot_B = L6206_Motor(tim_B, Pin.cpu.A0, Pin.cpu.A1, Pin.cpu.C1, 1, 2)
    
    # Enable the L6206 driver
    #mot_A.enable()
    #mot_B.enable()
    
    # Set the duty cycle of the first L6206 channel to 40 percent
    #mot_A.set_duty(50)
    #mot_B.set_duty(20)
    
    tim_A = Timer(3, freq = 20_000)
    tim_B = Timer(5, freq = 20_000)
    tim_C = Timer(4, freq = 20_000)
    A = L6206_Motor(tim_A, Pin.cpu.B4, Pin.cpu.B5, Pin.cpu.A10, 1, 2)
    B = L6206_Motor(tim_B, Pin.cpu.A0, Pin.cpu.A1, Pin.cpu.C1, 1, 2)
    C = L6206_Motor(tim_C, Pin.cpu.B6, Pin.cpu.B7, Pin.cpu.C1, 1, 2)
    A.set_duty(0)
    A.enable()
    B.set_duty(0)
    B.enable()
    C.set_duty(0)
    C.enable()
    print('Press "f" to fire')
    ser = pyb.USB_VCP()
    while True:
        if ser.any():
            charIn = ser.read(1).decode()
            if charIn in {'f'}:
                fire(A,B,C)
    





