import brickpi3
import sys
import time

brickPi = brickpi3.BrickPi3()

GYRO_SENSOR = brickPi.PORT_1
GYRO_INITIAL_VALUE = 2406

def exit(reason):
    print("Exiting... " + reason)
    brickPi.reset_all()
    sys.exit()
try:
    brickPi.set_sensor_type(GYRO_SENSOR, brickPi.SENSOR_TYPE.CUSTOM, [(brickPi.SENSOR_CUSTOM.PIN1_ADC)])
    while True:
        try:
            gyroOffset = brickPi.get_sensor(GYRO_SENSOR)[0] - GYRO_INITIAL_VALUE
            print("Gyro offset: " + str(gyroOffset))
            time.sleep(0.1)
        except brickpi3.SensorError as error:
            print("SensorError" , error)
        except IOError as error:
            print("IOError", error)
except KeyboardInterrupt:
    exit("Keyboard interrupt")
