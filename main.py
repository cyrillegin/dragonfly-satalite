from config import baseStation, sensors
from sensors.gpio import readTemp, setup

if __name__ == "__main__":
    print('hello world')
    print(baseStation)
    for i in sensors:
        print (i['name'])
        if i['sensor'] == 'gpio':
            print('go!')
            file = setup()
            temp = readTemp(file)
            print('temp is {}'.format(temp))
