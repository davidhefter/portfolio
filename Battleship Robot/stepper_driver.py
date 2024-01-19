'''!    @file stepper_driver.py
        @brief                                  A driver class from running stepper motors using the TMC4210 and TMC2208
                                                
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
                                                
        @date                                   November 8, 2022
'''

from pyb import Pin, SPI, Timer

'''!
    useful documentation:
           SPI:         https://docs.micropython.org/en/latest/library/pyb.SPI.html
           TMC4210:     https://www.trinamic.com/fileadmin/assets/Products/ICs_Documents/TMC4210_Datasheet_Rev.1.06.pdf
           TMC2208:     https://www.trinamic.com/fileadmin/assets/Products/ICs_Documents/TMC220x_TMC2224_datasheet_Rev1.09.pdf

'''
'''!
    Notes:
    
    from 4210 datasheet:
        For starting a motor proceed as follows:
            1. Set en_sd to 1 to enable the Step/Dir interface to the driver IC.
            2. Set the velocity parameters V_MIN and V_MAX.
            3. Set the clock pre-dividers PULSE_DIV and RAMP_DIV.
            4. Set A_MAX with a valid pair of PMUL and PDIV.
            5. Choose the ramp mode with RAMP_MODE register.
            6. Choose the reference switch configuration. Set mot1r to 1 for a left and a right reference
                switch. If this bit is not set and the right switch is not to be used, pull REF_R to GND.
            7. Now, the TMC4210 runs a motor if you write either X_TARGET or V_TARGET, depending on the
                choice of the ramp mode. 
                
            I think 1-6 can be in INIT
'''
class Stepper_Driver:
    '''!@brief      A driver class for the TMC4210 and TMC2208.

    '''

    def __init__ (self, timer_channel, timer, CLKpin, SPInum, CSpin1, CSmode1, CSvalue1, CSpin2, CSmode2, CSvalue2, ENpin1, ENpin2):
        '''!@brief     Initializes and returns an object associated with a stepper motor.
        '''
        
        ### STEPS I THINK WE NEED TO TAKE
        #
        #   1. Enable TMC2208
        #   2. Initialize and configure the TMC4210
        #       1. Set en_sd to 1 to enable the Step/Dir interface to the driver IC.
        #       2. Set the velocity parameters V_MIN and V_MAX.
        #       3. Set the clock pre-dividers PULSE_DIV and RAMP_DIV.
        #       4. Set A_MAX with a valid pair of PMUL and PDIV.
        #       5. Choose the ramp mode with RAMP_MODE register.
        #       6. Choose the reference switch configuration. Set mot1r to 1 for a left and a right reference
        #          switch. If this bit is not set and the right switch is not to be used, pull REF_R to GND.
        #
        ###
        
        self.degree_to_tick = 16015/3600
        
        # set up clock
        self.clk = timer.channel(timer_channel, timer.PWM, pin = CLKpin)
        
        # set up PWM
        self.clk.pulse_width_percent(50)
        
        # make CSpin usable
        self.CS1 = Pin(CSpin1, mode=CSmode1, value=CSvalue1)
        self.CS2 = Pin(CSpin2, mode=CSmode2, value=CSvalue2)
        
        # Enable
        Enable1 = Pin(ENpin1, mode=Pin.OUT_PP)
        Enable1.low()
        Enable2 = Pin(ENpin2, mode=Pin.OUT_PP)
        Enable2.low()
        
        # make spi usable
        self.SPI = SPI(SPInum, SPI.CONTROLLER, baudrate=115200, polarity=1, phase=1)
        
        # set interface configuration
        self.CS1.low()
        SMDA,IDX,RW=0b11,0b0100,0b0
        adr=SMDA<<5|IDX<<1|RW
        data = 0b00100000
        sdrcv = bytearray([adr, 0x00, 0x00, data])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS1.high()
        
        self.CS2.low()
        SMDA,IDX,RW=0b11,0b0100,0b0
        adr=SMDA<<5|IDX<<1|RW
        data = 0b00100000
        sdrcv = bytearray([adr, 0x00, 0x00, data])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS2.high()
        
        
        # set vmin
        self.CS1.low()
        SMDA,IDX,RW=0b00,0b0010,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, 0x00, 0x01])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS1.high()
        
        self.CS2.low()
        SMDA,IDX,RW=0b00,0b0010,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, 0x00, 0x01])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS2.high()
        
        
        # set vmax
        self.CS1.low()
        SMDA,IDX,RW=0b00,0b0011,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, 0x00, 0x0F])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS1.high()
        
        self.CS2.low()
        SMDA,IDX,RW=0b00,0b0011,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, 0x00, 0x0F])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS2.high()
        
        
        # set pulse_div and ramp_div
        self.CS1.low()
        pulsediv = 0b0011
        rampdiv = 0b0101
        data = pulsediv<<4|rampdiv
        SMDA,IDX,RW=0b00,0b1100,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, data, 0x00])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS1.high()
        
        self.CS2.low()
        pulsediv = 0b0011
        rampdiv = 0b0101
        data = pulsediv<<4|rampdiv
        SMDA,IDX,RW=0b00,0b1100,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, data, 0x00])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS2.high()
        
        
        # set amax
        self.CS1.low()
        SMDA,IDX,RW=0b00,0b0110,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, 0x00, 0x0F])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS1.high()
        
        self.CS2.low()
        SMDA,IDX,RW=0b00,0b0110,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, 0x00, 0x0F])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS2.high()
        
        
        # put motor in ramp mode and set ref_conf
        self.CS1.low()
        REF_CONF = 0b00001111
        R_M = 0b00000000 
        SMDA,IDX,RW=0b00,0b1010,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, REF_CONF, R_M])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS1.high()
        
        self.CS2.low()
        REF_CONF = 0b00001111
        R_M = 0b00000000 
        SMDA,IDX,RW=0b00,0b1010,0b0
        adr=SMDA<<5|IDX<<1|RW
        sdrcv = bytearray([adr, 0x00, REF_CONF, R_M])
        self.SPI.send_recv(sdrcv, recv=sdrcv)
        self.CS2.high()
        
        
    def set_position(self, mot_num, position):
        '''!@brief     Sets the target position for the motor to reach
        '''
        if mot_num==1:
            # set xtarget
            position = int(position*self.degree_to_tick)
            self.CS1.low()          # might need the self. to access cs and spi
            SMDA,IDX,RW=0b00,0b0000,0b0
            adr=SMDA<<5|IDX<<1|RW 
            sdrcv = bytearray(position.to_bytes(4, 'big'))
            #a = bytearray(position.to_bytes(4, 'big'))
            sdrcv[0] = adr
            #a[0]=adr
            self.SPI.send_recv(sdrcv, recv=sdrcv)
            self.CS1.high()
        elif mot_num==2:
            # set xtarget
            position = int(position*self.degree_to_tick)
            self.CS2.low()          # might need the self. to access cs and spi
            SMDA,IDX,RW=0b00,0b0000,0b0
            adr=SMDA<<5|IDX<<1|RW 
            sdrcv = bytearray(position.to_bytes(4, 'big'))
            #a = bytearray(position.to_bytes(4, 'big'))
            sdrcv[0] = adr
            #a[0]=adr
            self.SPI.send_recv(sdrcv, recv=sdrcv)
            self.CS2.high()
        #return [a, position]
        pass
    
    def set_velocity(v_max, v_min, v_target):
        '''!@brief     Sets the maximum, minimum, and target velocity of the stepper motor
        
            dont really care for our project but this would be useful functionality for future use
        '''
        pass
    
    def set_accel(v_max, v_min, v_target):
        '''!@brief     Sets the maximum, minimum, and target acceleration of the stepper motor
        
            dont really care for our project but this would be useful functionality for future use
        '''
        pass
    
    def get_position(self, mot_num):
        '''!@brief     Gets the current position for the motor
        '''
        if mot_num==1:
            self.CS1.low()
            SMDA,IDX,RW=0b00,0b0001,0b1
            adr=SMDA<<5|IDX<<1|RW
            sdrcv = bytearray([adr, 0x00, 0x00, 0x00])
            self.SPI.send_recv(sdrcv, recv=sdrcv)
            self.CS1.high()
            sdrcv = sdrcv[1:]
            position = str(int(int.from_bytes(sdrcv, "big")/self.degree_to_tick))
            return position
            #return sdrcv
        elif mot_num==2:
            self.CS2.low()
            SMDA,IDX,RW=0b00,0b0001,0b1
            adr=SMDA<<5|IDX<<1|RW
            sdrcv = bytearray([adr, 0x00, 0x00, 0x00])
            self.SPI.send_recv(sdrcv, recv=sdrcv)
            self.CS2.high()
            sdrcv = sdrcv[1:]
            position = str(int(int.from_bytes(sdrcv, "big")/self.degree_to_tick))
            return position
            #return sdrcv

if __name__ == "__main__":
    
    # set up timer
    timer = Timer(8, freq = 20000000)
    
    # Clock pin
    CLKpin = Pin.cpu.C7
    
    # set up SPI
    SPInum = 2
    #spi = SPI(2 = SPInum, SPI.CONTROLLER, baudrate=115200, polarity=1, phase=1)
    
    # CS pin
    CSpin = Pin.cpu.B7
    # CS operating mode, ie in or out
    CSmode = Pin.OUT_PP
    # CS initial value
    CSvalue = 1
    #CS = Pin(Pin.cpu.B7, mode=Pin.OUT_PP, value=1)
    
    # Enable pin
    ENpin = Pin.cpu.B6
    # ENpin = Pin(Pin.cpu.B6, mode=Pin.OUT_PP, value=0)
    
    
    stepper = Stepper_Driver(2, timer, CLKpin, SPInum, CSpin, CSmode, CSvalue, ENpin)
    
    stepper.set_position(1000)
    
    
    