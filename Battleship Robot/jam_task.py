'''!    @file jam_task.py
        @brief                                  Uses a IR break beam sensor to see if a ball has left the barrel
                                                
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
                                                
        @date                                   November 15, 2022
'''

from pyb import Pin
import time

# need to power the sensors
# set two pins high, two pins low

def JamTaskFcn(FireSignal, jam):
    
    break_beam = Pin( Pin.cpu.B0, mode = Pin.IN, pull=Pin.PULL_UP, value = None )
    
    state = 0
    
    while True:
        
        if state == 0:
            # check for fire signal
            # start timer
            # go into state 1
            
            if FireSignal.get():
                start_time = time.ticks_us()
                FireSignal.put(False)
                state = 1
            
        elif state == 1:
            # check jam sensor
            # if jam sensor = 1 and current time is greater than start time >>> jam flag = true
            
            current_time = time.ticks_us()
            
            if current_time > start_time + 6_000_000:
                state = 0
                jam.put(True)
            elif break_beam.value() == 0:
                state = 0
            
        yield

if __name__ == '__main__':
    break_beam = Pin( Pin.cpu.B0, mode = Pin.IN, pull=Pin.PULL_UP, value = None )
    

    while True:
        
        ball_sensed = break_beam.value()
        
        print(ball_sensed)