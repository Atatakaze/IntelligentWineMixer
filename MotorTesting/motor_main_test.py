##################################################
#                                                #
# Program:					 #
#	check whether the motor worls properly   #
#       motor_main_test.py                       #
# History:                                       #
#       2021/09/14                               #
# < using 4-steps step motor >                   #
#                                                #
##################################################

from motor_function_test import motor_init, motor_run, motor_param

# <motor parameter setting> 
#     <set motor output pins> 
motor1 = [17, 18, 27, 22] 
motor2 = [10, 9, 11, 8]
#     </set motor output pins>      
# </motor parameter setting> 

if __name__ == "__main__":
    
    # setting motor speed and duration
    # >>> python motor_main.py <motor1 speed> <motor1 duration> <motor2 speed> <motor2 duration>
    motor1_speed, motor1_duration, motor2_speed, motor2_duration = motor_param()

    # initial motor 1
    motor1_SEQUENCE, motor1_SEQUENCE_COUNT, motor1_PIN_COUNT = motor_init(motor1)
    # initial motor 2
    motor2_SEQUENCE, motor2_SEQUENCE_COUNT, motor2_PIN_COUNT = motor_init(motor2)
    
    # program start
    try:
        print('Ress Ctrl-C to stop the program.')
        while True:
            # select motor
            motorSelect = int(input('Select which motor to run (1: motor1, 2: motor 2): '))
            # select direction
            direction = int(input('Select which direction to run (1: clockwise, -1: counterwise): '))
            if motorSelect == 1:
                # motor_run(motor, Direction, SEQUENCE, Duration, Speed, SEQUENCE_COUNT, PIN_COUNT)
                motor_run(motor1, direction, motor1_SEQUENCE, motor1_duration, motor1_speed, motor1_SEQUENCE_COUNT, motor1_PIN_COUNT)
            if motorSelect == 2:
                # motor_run(motor, Direction, SEQUENCE, Duration, Speed, SEQUENCE_COUNT, PIN_COUNT)
                motor_run(motor2, direction, motor2_SEQUENCE, motor2_duration, motor2_speed, motor2_SEQUENCE_COUNT, motor2_PIN_COUNT)
            
    except KeyboardInterrupt:  
        print('Program Closed.')
    finally:
        gpio.cleanup()
