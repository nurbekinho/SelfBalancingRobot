import brickpi3
import sys
import time

brickPi = brickpi3.BrickPi3()

RIGHT_MOTOR = brickPi.PORT_A
LEFT_MOTOR = brickPi.PORT_D

def exit(reason):
    print("Exiting... " + reason)
    brickPi.reset_all()
    sys.exit()

try:
    brickPi.offset_motor_encoder(LEFT_MOTOR, brickPi.get_motor_encoder(LEFT_MOTOR))
    brickPi.offset_motor_encoder(RIGHT_MOTOR, brickPi.get_motor_encoder(RIGHT_MOTOR))
    while True:
        try:
            leftMotorPosition = brickPi.get_motor_encoder(LEFT_MOTOR)
            rightMotorPosition = brickPi.get_motor_encoder(RIGHT_MOTOR)
            print("Left motor position: " + str(leftMotorPosition) + " Right motor position: " + str(rightMotorPosition))
            brickPi.set_motor_power(LEFT_MOTOR , 50)
            time.sleep(0.5)
        except brickpi3.SensorError as error:
            print("SensorError" , error)
        except IOError as error:
            print("IOError", error)
except KeyboardInterrupt:
    exit("Keyboard interrupt")
