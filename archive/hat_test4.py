#https://projects.raspberrypi.org/en/projects/sense-hat-data-logger

from sense_hat import SenseHat
from datetime import datetime
import sched, time
import csv
#from csv import writer




sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

# Function to return all parameters
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

# Special symbol        
degree_sign= u'\N{DEGREE SIGN}'

# Writes data to screen
def write_data(a):

  now = datetime.now()
  date_time_string = now.strftime("%Y-%m-%d, %H:%M:%S")

  # Color sensor values
  temperature = "{0:.2f}".format(sense.get_temperature()) 
  humidity = "{0:.2f}".format(sense.get_humidity())
  pressure = "{0:.2f}".format(sense.get_pressure())

  # Read sensor
  orientation = sense.get_orientation()
  mag = sense.get_compass_raw()
  acc = sense.get_accelerometer_raw()
  gyro = sense.get_gyroscope_raw()
  
  # Collect specific sensor data
  yaw = str("{0:.3f}".format(orientation['yaw']))
  pitch = str("{0:.3f}".format(orientation['pitch']))
  roll = str("{0:.3f}".format(orientation['roll']))
  mag_x = str("{0:.3f}".format(mag['x']))
  mag_y = str("{0:.3f}".format(mag['y']))
  mag_z = str("{0:.3f}".format(mag['z']))
  acc_x = str("{0:.3f}".format(acc["x"]))
  acc_y = str("{0:.3f}".format(acc["y"]))
  acc_z = str("{0:.3f}".format(acc["z"]))
  gyro_x = str("{0:.3f}".format(gyro["x"]))
  gyro_y = str("{0:.3f}".format(gyro["y"]))
  gyro_z = str("{0:.3f}".format(gyro["z"]))
  
  # Construct formatted output
  sep = ", "
  #print ('Date, Time, Temp, Humidity, Pressure, Yaw, Pitch, Roll, MagX, MagY, MagZ, AccX, AccY, AccZ, GyroX, GyroY, GyroZ')
  parameters = [date_time_string, temperature, humidity, pressure, yaw, pitch, roll,
  mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
  
  output = sep.join(parameters)
  fout = open('data/sensor.txt', 'a')
  fout.write(parameters + '\n')
  fout.close()
  
  #print (output)

# Run code at fixed time interval
while True:
  schedule.enter(0.5,1,write_data,('params',))
  schedule.run()

        