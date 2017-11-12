#https://projects.raspberrypi.org/en/projects/sense-hat-data-logger

from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()

def get_sense_data():
  sense_data = []
  
  sense_data.append(sense.get_temperature())
  sense_data.append(sense.get_pressure())
  sense_data.append(sense.get_humidity())
  orientation = sense.get_orientation()
  sense_data.append(orientation["yaw"])
  sense_data.append(orientation["pitch"])
  sense_data.append(orientation["roll"])
  mag = sense.get_compass_raw()
  sense_data.append(mag["x"])
  sense_data.append(mag["y"])
  sense_data.append(mag["z"])
  acc = sense.get_accelerometer_raw()
  sense_data.append(acc["x"])
  sense_data.append(acc["y"])
  sense_data.append(acc["z"])
  gyro = sense.get_gyroscope_raw()
  sense_data.append(gyro["x"])
  sense_data.append(gyro["y"])
  sense_data.append(gyro["z"])
  return sense_data

        
degree_sign= u'\N{DEGREE SIGN}'
        
while True:
  #print(get_sense_data())        
  #print ("Temperature: {0:.3f}".format(sense.get_temperature()))
  temperature = "{0:.2f}".format(sense.get_temperature()) + degree_sign + "C"
  humidity = "{0:.2f}".format(sense.get_humidity()) + "%"
  pressure = "{0:.2f}".format(sense.get_pressure()) + " mB"
  sep = ","
  parameters = [temperature, humidity, pressure]
  output = sep.join(parameters)
  print (output)
  
  
        
        