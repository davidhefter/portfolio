'''!    @file shoot_task.py
        @brief                                  controls two shooting wheels and linear actuator
                                                
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
                                                
        @date                                   November 28, 2022
'''
import time
import L6206_Motor
from pyb import Pin, Timer

def ShootTaskFcn( FireSignal, LoadSignal ):
    
    state = 0
    start_time = time.ticks_ms()
    
    while True:
        
        # STATE 0: INIT
        if state == 0:
            # set up 3 motor objects
            # go to state = 1
            
            # Motor timers
            tim_A = Timer(3, freq = 20_000)
            tim_B = Timer(5, freq = 20_000)
            tim_C = Timer(4, freq = 20_000)
            
            # Motor objects
            mot_A = L6206_Motor.L6206_Motor(tim_A, Pin.cpu.B4, Pin.cpu.B5, Pin.cpu.A10, 1, 2)
            mot_B = L6206_Motor.L6206_Motor(tim_B, Pin.cpu.A0, Pin.cpu.A1, Pin.cpu.C1, 1, 2)
            mot_C = L6206_Motor.L6206_Motor(tim_C, Pin.cpu.B6, Pin.cpu.B7, Pin.cpu.C1, 1, 2)
            
            # enable motors
            mot_A.enable() # shooter left
            mot_B.enable() # shooter right
            mot_C.enable() # linear
            
            mot_A.set_duty(0)
            mot_B.set_duty(0)
            mot_C.set_duty(-100)
            
            # transition to state 1
            if time.ticks_ms() > start_time + 1000:
                mot_C.set_duty(0)
                state = 1
        
        # STATE 1: WAIT_TO_LOAD
        elif state == 1:
            # wait for load signal
            # go into load sequence
            if LoadSignal.get():
                start_time = time.ticks_ms()
                mot_C.set_duty(100)
                state = 2
                
        # STATE 2: LOAD    
        elif state == 2:
            # load cannon
            # second: after 0.30s more, halt linear to not extend fully
            if time.ticks_ms() > start_time+1200:
                mot_C.set_duty(0)
                state = 3
                LoadSignal.put(False)
            # first: after 0.90s push linear forward to block balls
            elif time.ticks_ms() > start_time+900:
                mot_C.set_duty(-100)
        
        # STATE 3: WAIT TO SHOOT
        elif state == 3:
            # wait for fire signal
            # go into fire sequence
            if FireSignal.get():
                mot_A.set_duty(100)
                mot_B.set_duty(100)
                state = 4
                start_time = time.ticks_ms()
        
        # STATE 4: SHOOT        
        elif state == 4:
            # fire cannon
            # second: after 1.00s more, halt motors
            if time.ticks_ms() > start_time+2200:
                mot_A.set_duty(0)
                mot_B.set_duty(0)
                mot_C.set_duty(0)
                state = 1
            # first: after 1.20s push linear fully to fire cannon
            elif time.ticks_ms() > start_time+1200:
                mot_C.set_duty(-100)
            
            #### this is for testing without jam task 
            #FireSignal.put(False)
            ####
            
            
        yield