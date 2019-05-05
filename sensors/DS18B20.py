import time
import logging
import os
import glob

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.INFO)


def setupGPIO():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # This will need to change if there are more
    # than one onewire devices connected
    # TODO: make this configurable to allow for multiple sensors
    deviceFolder = glob.glob('/sys/bus/w1/devices/28*')[0]
    deviceFile = deviceFolder + '/w1_slave'
    return deviceFile


def readTempRaw(deviceFile):
    f = open(deviceFile, 'r')
    lines = f.readlines()
    f.close()
    return lines


def readTemp(deviceFile):
    lines = readTempRaw(deviceFile)

    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempRaw()

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f


if __name__ == '__main__':
    while True:
        print(readTemp())
        time.sleep(1)
