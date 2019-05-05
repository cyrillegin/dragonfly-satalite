import time
import logging
import os
import glob

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.INFO)


def setup():
    # Made sure `dtoverlay=w1-gpio` is in /boot/config.txt (requires reboot)
    # run:
        # sudo modprobe w1-gpio
        # sudo modprobe w1-therm
        # cd /sys/bus/w1/devices
        # ls
    # There should be a folder starting with 28-
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    deviceFolder = glob.glob('/sys/bus/w1/devices/28*')[0]
    deviceFile = deviceFolder + '/w1_slave'
    print('done setting up')
    return deviceFile


# A function that reads the sensors data
def readTempRaw(deviceFile):
    f = open(deviceFile, 'r')
    lines = f.readlines()
    f.close()
    return lines


# Convert the value of the sensor into a temperature
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
