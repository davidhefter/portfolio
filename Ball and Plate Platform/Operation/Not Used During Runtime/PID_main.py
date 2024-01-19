### THIS CODE WAS ONLY USED FOR MOVING THE MOTOR AND OUTPUTTING POSITION/TIME DATA FOR TUNING THE CONTROLLER ###
### THIS FILE ISN'T USED IN THE MAIN CODE ###
import pyb 
from pyb import Pin, Timer, ADC, UART, SPI
import micropython
import ustruct
import utime
from motor_driver import Motor_Driver
from encoder_reader import Encoder_Reader
from pi_control import PI_Control
import math
import utime
import gc
import pyb
from pyb import Pin, Timer, ADC, UART, SPI
from machine import I2C

# Motors 1 and 2

## M12TIM
tim3 = Timer(3, freq = 20000)

# Motor 1

## M1PWM pin (PWM)
PC6 = Pin(Pin.cpu.C6, mode=Pin.ALT, af=2)
## M1DIR pin (direction)
PC7 = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)
## M1!SLP pin (set high to unsleep driver)
PC13 = Pin(Pin.cpu.C13, mode=Pin.OUT_OD)
## M1!FLT pin (goes low when there's a fault)
PC2 = Pin(Pin.cpu.C2)#, mode=Pin.IN, pull=Pin.PULL_UP)
## M1CS pin (current sensor)
PC0 = Pin(Pin.cpu.C0, mode=Pin.ANALOG)
## M1CS ADC (current sensor)
M1CS = ADC(PC0)
## M1PWM timer channel
ch3_1 = tim3.channel(1, mode=Timer.PWM)

# Motor 2

## M2PWM pin
PB0 = Pin(Pin.cpu.B0, mode=Pin.ALT, af=2)
## M2DIR pin
PB1 = Pin(Pin.cpu.B1, mode=Pin.OUT_PP)
## M2!SLP pin
PB4 = Pin(Pin.cpu.B4, mode=Pin.OUT_OD)
## M2!FLT pin
PB5 = Pin(Pin.cpu.B5, mode=Pin.IN, pull=Pin.PULL_UP)
## M2CS pin
PC1 = Pin(Pin.cpu.C1, mode=Pin.ANALOG)
## M2CS ADC
M2CS = ADC(PC1)
## M2PWM timer channel
ch3_3 = tim3.channel(3, mode=Timer.PWM)


# Encoders 1 and 2

## Encoder 1

## E1TIM
tim4 = Timer(4, period=0xFFFF, prescaler=0, mode=Timer.UP)
## E1CHA pin
PB6 = Pin(Pin.cpu.B6, mode=Pin.ALT, af=2)
## E1CHB pin
PB7 = Pin(Pin.cpu.B7, mode=Pin.ALT, af=2)
## E1CHA timer channel
E1CHA = tim4.channel(1, mode=Timer.ENC_AB)
## E1CHB timer channel
E1CHB = tim4.channel(2, mode=Timer.ENC_AB)
## Encoder 1 position
E1POS = 0
## Encoder 1 timer count
E1CNT = tim4.counter()
## Encoder 1 change in position
E1DELTA = 0
## E1 Callback
def E1CB(irq_src):
    global E1POS, E1CNT, E1DELTA, tim4

    E1OLD = E1CNT
    E1CNT = tim4.counter()
    # E1DELTA = E1CNT - E1OLD
    E1DELTA = E1OLD - E1CNT
    if E1DELTA > 32767:
        E1DELTA -= 65536
    elif E1DELTA < -32768:
        E1DELTA += 65536
    E1POS += E1DELTA
## E1 interrupt timer
#tim6 = Timer(6, freq=512, callback=E1CB)
tim6_chan = 6
tim6_freq = 512

# Encoder 2

## E2TIM
tim5 = Timer(5, period=0xFFFF, prescaler=0, mode=Timer.UP)
## E2CHA pin
PA0 = Pin(Pin.cpu.A0, mode=Pin.ALT, af=2)
## E2CHB pin
PA1 = Pin(Pin.cpu.A1, mode=Pin.ALT, af=2)
## E2CHA timer channel
E2CHA = tim5.channel(1, mode=Timer.ENC_AB)
## E2CHB timer channel
E2CHB = tim5.channel(2, mode=Timer.ENC_AB)
## E2 Position
E2POS = 0
## E2 timer count
E2CNT = tim5.counter()
## E2 change in encoder position
E2DELTA = 0
## E2 callback
def E2CB(irq_src):
    global E2POS, E2CNT, E2DELTA, tim5

    E2OLD = E2CNT
    E2CNT = tim5.counter()
    # E2DELTA = E2CNT - E2OLD
    E2DELTA = E2OLD - E2CNT
    if E2DELTA > 32767:
        E2DELTA -= 65536
    elif E2DELTA < -32768:
        E2DELTA += 65536
    E2POS += E2DELTA
## E2 interrupt timer
#tim7 = Timer(7, freq=512, callback=E2CB)
tim7_chan = 7
tim7_freq = 512


# Allocate some memory for exceptions that occur inside interrupts
micropython.alloc_emergency_exception_buf(100)

# Create both motor drivers
motorA = Motor_Driver(tim3, PC6, PC7, PC13, PC2, PC0, M1CS, ch3_1)
motorB = Motor_Driver(tim3, PB0, PB1, PB4, PB5, PC1, M2CS, ch3_3)
encoderA = Encoder_Reader(tim4, PB6, PB7, tim6_chan, tim6_freq)
encoderB = Encoder_Reader(tim5, PA0, PA1, tim7_chan, tim7_freq)

Kp=0.025
Ki=0.00030
Kd=0.00085

controllerA = PI_Control(Kp, Ki, Kd, 0, encoderA, motorA)
controllerB = PI_Control(Kp, Ki, Kd, 0, encoderB, motorB)

itime = utime.ticks_ms()
motorA.enable()
tpd = 4096/360
target = 15*tpd # degree*tick/degree=tick
end_target=0
rate = -10*tpd # dps * tpd = tps
duty_cycle=30
ser = pyb.USB_VCP()
motorA.disable()
motorB.disable()

# Note that A and B go opposite directions, 
# so if you run A at rate R, then you should run B -1*R to go the same direction

# Code to run step or first order step input
while utime.ticks_ms()- itime < 1000:
        utime.sleep_ms(2)
        controllerA.run(target)                                 # for step only
        #controllerA.run(rate*(utime.ticks_ms()- itime))        # for first order only
        motorA.set_duty_cycle(controllerA.pwm)                  
        print(utime.ticks_ms()- itime, ",", encoderA.read())
print("end run")

itime = utime.ticks_ms()
utime.sleep_ms(3000)
   
motorA.set_duty_cycle(0)
