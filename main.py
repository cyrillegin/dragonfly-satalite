import time
from multiprocessing import Process
import requests
import logging
from config import baseStation, sensors
from sensors.DS18B20 import readTemp, setupGPIO

runningSensors = []

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.INFO)


def sendToServer(sensor, data):
    payload = {
        'value': data,
        'timestamp': time.time(),
        'sensorName': sensor['sensor'],
        'stationName': sensor['station']
    }
    response = requests.post('http://{}/api/reading'.format(baseStation), data=payload)
    logging.debug(response)


def pollData(sensor, config):
    while True:
        data = None
        if sensor['sensor'] == 'DS18B20':
            data = readTemp(config)

        if data is None:
            logging.error('sensor not setup correctly')

        sendToServer(sensor, data)
        # TODO: Move this to config
        time.sleep(5)


def setupSensor(sensor):
    print(sensor)
    if sensor['sensor'] == 'DS18B20':
        return setupGPIO()


if __name__ == "__main__":
    while True:
        logging.debug('Checking for new sensors')
        index = 0
        for i in sensors:
            if len(runningSensors) < index + 1:
                runningSensors.append(None)
            if runningSensors[index] is None or not runningSensors[index].is_alive():
                config = setupSensor(i)
                p = Process(target=pollData, args=(i, config, ))
                p.start()
                runningSensors[index] = p
            index += 1
        # Check every five minutes
        time.sleep(60 * 5)
