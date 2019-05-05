# Dragonfly Satellite

Repository containing code used for pulling data from raspberry pis.
This should be cloned directly on to the pi.

To get started, copy the contents of config-template.py into a new file called config.py
Make sure to change the baseStation parameter to point to where ever you have the main dragonfly framework running.

Once you've added your sensors to the config, run `python main.py` to start collecting data.


### Sensors

All sensors have a base config requiring a sensor, station, and name in the following format:
```
{
  'name': 'name-of-sensor',
  'sensor': 'type-of-sensor',
  'station': 'name-of-station',
}
```
The name and station properties can be whatever you'd like however the sensor attribute must be tied to a particular sensor that is supported.

#### DS18B20 Temperature Sensor
sensor name: 'DS18B20'
