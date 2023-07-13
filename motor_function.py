#!/usr/bin/python3
# Program:
#       Providing GUI_main.py and motor_main.py with functions for opening and closing burette.
# Author:
#	bobo
# History:
#       2022/04/11	@bobo


import RPi.GPIO as GPIO
import time
import sys

# calculating the duration needed for the target volume
def calVolume(motor, volume):
    if motor == 'MOTOR1':
        duration = ( volume - 5.4 ) / 6.08
    elif motor == 'MOTOR2':
        duration = ( volume - 3.87 ) / 0.42
    return duration

# mixing two wine
# wine1:wine2 = the ratio of two wine in the mix (unit: ml)
def Mixing(wine1, wine2):
    duration1 = calVolume('MOTOR1', wine1)
    duration2 = calVolume('MOTOR2', wine2)
    return duration1, duration2

# initial parameters from sys.argv
# setting motor speed and duration
# >>> python motor_main.py <motor1 duration> <motor2 duration>
def motor_param():
    # only one parameter -> steps of motor 1, steps of motor 2 remains default, 100. 
    if len(sys.argv) == 2:  
        MOTOR1_STEPS = int(sys.argv[1])
        MOTOR2_STEPS = 100
    # two parameter -> steps of motor 1, steps of motor 2 
    elif len(sys.argv) == 3:
        MOTOR1_STEPS = int(sys.argv[1])
        MOTOR2_STEPS = int(sys.argv[2])
    # two parameter -> steps of motor 1, steps of motor 2 both remain default, 100. 
    else:
        MOTOR1_STEPS = 100
        MOTOR2_STEPS = 100
    return MOTOR1_STEPS, MOTOR2_STEPS

# initial output pins of motors
def motor_init(OUTPUTPINS):
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    for pin in range(4):
        # set OUTPUTPINS as output
        GPIO.setup(OUTPUTPINS[pin], GPIO.OUT)
        # initial OUTPUTPINS to 0
        GPIO.output(OUTPUTPINS[pin], GPIO.LOW)
    # step motor sequence
    
    SEQUENCE = [[1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
                [1, 0, 0, 1]]
    SEQUENCE_COUNT = len(SEQUENCE)
    PIN_COUNT = len(OUTPUTPINS)
    
    return SEQUENCE, SEQUENCE_COUNT, PIN_COUNT
    
# motor running
# <OUTPUTPINS> select which motor to run
# <MODE> [mode1] clockwise -> counterwise, [mode2] counterwise -> clockwise 
# <DURATION> the time that burette remains open
# <MOTOR_STEPS> how many steps the motor need to run
# <SEQUENCE> [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
# <SEQUENCE_COUNT> 4
# <PIN_COUNT> 4
def motor_run(OUTPUTPINS, MODE, DURATION, MOTOR_STEPS=100, SEQUENCE=[[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]], SEQUENCE_COUNT=4, PIN_COUNT=4):
    
    sequence_index = 0
    steps_count = 0
    # select mode
    if MODE == 1:
        open_direction = 1
        close_direction = -1
    elif MODE == 2:
        open_direction = -1
        close_direction = 1
    else:
        print('MODE1 or MODE2')
        return 0
        
    # open burette
    print('Open ...')
    while steps_count < MOTOR_STEPS:
        for pin in range(PIN_COUNT):
            GPIO.output(OUTPUTPINS[pin], SEQUENCE[sequence_index][pin])
            time.sleep(0.01)
        
        sequence_index += open_direction
        sequence_index %= SEQUENCE_COUNT
        
        time.sleep(10/float(1000))
        steps_count += 1
        print('open progress: ', steps_count, '%')
    
    if DURATION < 0:
        DURATION = 0
    print('Halt for ', DURATION, ' seconds...')
    time.sleep(DURATION)
    
    # close burette
    steps_count = 0
    print('Close ...')
    while steps_count < MOTOR_STEPS:
        for pin in range(PIN_COUNT):
            GPIO.output(OUTPUTPINS[pin], SEQUENCE[sequence_index][pin])
            time.sleep(0.01)
        
        sequence_index += close_direction
        sequence_index %= SEQUENCE_COUNT
        
        time.sleep(10/float(1000))
        steps_count += 1
        print('close progress: ', steps_count, '%')
    
    print('Finish !!! ')
