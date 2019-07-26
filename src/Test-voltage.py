import brickpi3
import sys
import time

brickPi = brickpi3.BrickPi3()

def exit(reason):
    print("Exiting... " + reason)
    brickPi.reset_all()
    sys.exit()
try:
    while True:
        try:
            print("voltage:", brickPi.get_voltage_battery())
            time.sleep(1)
        except brickpi3.SensorError as error:
            print("SensorError" , error)
        except IOError as error:
            print("IOError", error)
except KeyboardInterrupt:
    exit("Keyboard interrupt")
