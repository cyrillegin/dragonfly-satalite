from config import baseStation, sensors

if __name__ == "__main__":
    print('hello world')
    print(baseStation)
    for i in sensors:
        print (i['name'])
