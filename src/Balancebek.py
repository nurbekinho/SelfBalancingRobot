import brickpi3
import sys
import time

brickPi = brickpi3.BrickPi3()

GYRO_SENSOR = brickPi.PORT_1
RIGHT_MOTOR = brickPi.PORT_A
LEFT_MOTOR = brickPi.PORT_D

LOOP_TIME = 0.01
GYROSPEEDCORRECT = 0.25
GYROANGLECORRECT = 0.25
KGYROANGLE = 14
KGYROSPEED = 1.2
KPOS       = 0.07
KSPEED     = 0.1
KSTEER     = 0.25

def exit(reason):
    print("Exiting... " + reason)
    brickPi.reset_all()
    sys.exit()

try:
    if brickPi.get_voltage_battery() < 7: exit("At least 7V of voltage is needed to run the motors! Current voltage: " + str(brickPi.get_voltage_battery()))

    brickPi.offset_motor_encoder(LEFT_MOTOR, brickPi.get_motor_encoder(LEFT_MOTOR))
    brickPi.offset_motor_encoder(RIGHT_MOTOR, brickPi.get_motor_encoder(RIGHT_MOTOR))
    brickPi.set_sensor_type(GYRO_SENSOR, brickPi.SENSOR_TYPE.CUSTOM, [(brickPi.SENSOR_CUSTOM.PIN1_ADC)])

    gyroOffset = 2406 # initial value of Gyro sensor
    gyroAngle = 0
    sumOfMotorPositions = 0
    motorPosition = 0
    deltaOfMotorPositions = 0

    while True:
        try:
            gyroChangeAngle = (brickPi.get_sensor(GYRO_SENSOR)[0] - gyroOffset) / 4
            gyroOffset += gyroChangeAngle * GYROSPEEDCORRECT * LOOP_TIME
            gyroAngle += gyroChangeAngle * LOOP_TIME - (gyroAngle * GYROANGLECORRECT * LOOP_TIME)

            leftMotorPosition = brickPi.get_motor_encoder(LEFT_MOTOR)
            rightMotorPosition = brickPi.get_motor_encoder(RIGHT_MOTOR)
            previousSumOfMotorPositions = sumOfMotorPositions
            sumOfMotorPositions = leftMotorPosition + rightMotorPosition
            differenceOfMotorPositions = leftMotorPosition - rightMotorPosition
            deltaOfMotorPositions = sumOfMotorPositions - previousSumOfMotorPositions
            motorPosition += deltaOfMotorPositions
            motorSpeed = deltaOfMotorPositions / LOOP_TIME

            power = KGYROSPEED * gyroChangeAngle + KGYROANGLE * gyroAngle + KPOS * motorPosition + KSPEED * motorSpeed
            if abs(power) > 1000: exit("Robot fell!")
            
            powerSteer = -differenceOfMotorPositions * KSTEER
            powerLeft = power + powerSteer
            powerRight = power - powerSteer
            
            if powerLeft > 100: powerLeft = 100
            if powerLeft < -100: powerLeft = -100
            if powerRight > 100: powerRight = 100
            if powerRight < -100: powerRight = -100
            
            brickPi.set_motor_power(LEFT_MOTOR , powerLeft)
            brickPi.set_motor_power(RIGHT_MOTOR, powerRight)
            time.sleep(LOOP_TIME) 
        except brickpi3.SensorError as error:
            print("SensorError" , error)
        except IOError as error:
            print("IOError", error)
except KeyboardInterrupt:
    exit("Keyboard interrupt")
