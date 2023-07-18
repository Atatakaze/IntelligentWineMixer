#########################################################
#                                                	#
# Program:                                       	#
#       checking whether the motor works properly 	#
#	functions used by motor_main_test.py    	#
# History:                                       	#
#       2021/09/14                               	#
# < using 4-steps step motor >                   	#
#                                                	#
#########################################################

import RPi.GPIO as GPIO
import time
import sys

# initial parameters from sys.argv
# setting motor speed and duration
# >>> python motor_main.py <motor1 speed> <motor1 duration> <motor2 speed> <motor2 duration>
def motor_param():
    if len(sys.argv) == 2:
        motor1_speed = int(sys.argv[1])/float(1000)
        motor1_duration = 100
        motor2_speed = 10/float(1000)
        motor2_duration = 100
    elif len(sys.argv) == 3:
        motor1_speed = int(sys.argv[1])/float(1000)
        motor1_duration = int(sys.argv[2])
        motor2_speed = 10/float(1000)
        motor2_duration = 100
    elif len(sys.argv) == 4:
        motor1_speed = int(sys.argv[1])/float(1000)
        motor1_duration = int(sys.argv[2])
        motor2_speed = int(sys.argv[3])/float(1000)
        motor2_duration = 100
    elif len(sys.argv) == 5:
        motor1_speed = int(sys.argv[1])/float(1000)
        motor1_duration = int(sys.argv[2])
        motor2_speed = int(sys.argv[3])/float(1000)
        motor2_duration = int(sys.argv[4])
    else:
        motor1_speed = 10/float(1000)
        motor1_duration = 100
        motor2_speed = 10/float(1000)
        motor2_duration = 100
    return motor1_speed, motor1_duration, motor2_speed, motor2_duration

# initial output pins of motors
def motor_init(OutputPins):
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    for pin in range(4):
        # set OutputPins as output
        GPIO.setup(OutputPins[pin], GPIO.OUT)
        # initial OutputPins to 0
        GPIO.output(OutputPins[pin], GPIO.LOW)
    # step motor sequence
    
    SEQUENCE = [[1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
                [1, 0, 0, 1]]
    SEQUENCE_COUNT = len(SEQUENCE)
    PIN_COUNT = len(OutputPins)
    
    return SEQUENCE, SEQUENCE_COUNT, PIN_COUNT
    
# motor running
def motor_run(OutputPins, Direction, SEQUENCE, Duration=100, Speed=(10/float(1000)), SEQUENCE_COUNT=4, PIN_COUNT=4):
    
    print('Start working ...')
    sequence_index = 0
    duration_count = 0
    
    while duration_count < Duration:
        for pin in range(PIN_COUNT):
            GPIO.output(OutputPins[pin], SEQUENCE[sequence_index][pin])
            time.sleep(0.01)
            
        sequence_index += Direction
        sequence_index %= SEQUENCE_COUNT
        
        print('progress:', duration_count)
        time.sleep(Speed)
        duration_count += 1
    
    print('Finished !!!')
     
