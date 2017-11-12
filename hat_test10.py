#https://projects.raspberrypi.org/en/projects/sense-hat-data-logger

from sense_hat import SenseHat, ACTION_HELD, ACTION_PRESSED, ACTION_RELEASED
from datetime import datetime
import sched, time
import csv

sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

# Special symbol        
degree_sign= u'\N{DEGREE SIGN}'

# global vars
walking = 0
enable_data_logging = 0
list_data = []
row_count = 0

# Build filename
now = datetime.now()
date_string = now.strftime("%m_%d_%Y")
time_string = now.strftime("%H_%M_%S")
filename = "data/sensor_" + date_string + "_" + time_string + ".csv"

# Write header
header = 'DateTime, Temp, Humidity, Pressure, Yaw, Pitch, Roll, MagX, MagY, MagZ, AccX, AccY, AccZ, GyroX, GyroY, GyroZ, State'  
list_data.append(header)

# Writes data to screen
def write_data(name):
  global walking
  global enable_data_logging
  global list_data
  global row_count
  
  if enable_data_logging == 0:
    return
    
  now = datetime.now()
  date_string = now.strftime("%m/%d/%Y")
  time_string = now.strftime("%H:%M:%S.%f")
  date_time_string = now.strftime("%m/%d/%Y %H:%M:%S.%f")
  
  # Color sensor values
  temperature = "{0:.3f}".format(sense.get_temperature()) 
  humidity = "{0:.3f}".format(sense.get_humidity())
  pressure = "{0:.3f}".format(sense.get_pressure())

  # Read sensor
  orientation = sense.get_orientation()
  mag = sense.get_compass_raw()
  acc = sense.get_accelerometer_raw()
  gyro = sense.get_gyroscope_raw()
  
  # Collect specific sensor data
  yaw = str("{0:.6f}".format(orientation['yaw']))
  pitch = str("{0:.6f}".format(orientation['pitch']))
  roll = str("{0:.6f}".format(orientation['roll']))
  mag_x = str("{0:.6f}".format(mag['x']))
  mag_y = str("{0:.6f}".format(mag['y']))
  mag_z = str("{0:.6f}".format(mag['z']))
  acc_x = str("{0:.6f}".format(acc["x"]))
  acc_y = str("{0:.6f}".format(acc["y"]))
  acc_z = str("{0:.6f}".format(acc["z"]))
  gyro_x = str("{0:.6f}".format(gyro["x"]))
  gyro_y = str("{0:.6f}".format(gyro["y"]))
  gyro_z = str("{0:.6f}".format(gyro["z"]))
  
  # Construct formatted output
  parameters = [date_time_string, temperature, humidity, pressure, yaw, pitch, roll,
  mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, walking]
  
  output = ','.join(str(x) for x in parameters) #sep.join(parameters)
  row_count += 1
  #print (output)
  
  # Append data
  list_data.append(output)
  return

def read_joystick(name):
  global walking
  global enable_data_logging
  
  for event in sense.stick.get_events():
    if event.action == ACTION_HELD and event.direction == "middle":
      walking = 1
    else:
      walking = 0
    
    # stop data logging
    if event.action == ACTION_PRESSED and event.direction == "down":  
      print ("Data logging disabled")
      enable_data_logging = 0
    elif event.action == ACTION_PRESSED and event.direction == "up":  
      print ("Data logging enabled")
      enable_data_logging = 1
    #elif event.action == ACTION_PRESSED and event.direction == "left":  
    #  print ("left")
    #elif event.action == ACTION_PRESSED and event.direction == "right":  
    #  print ("right")    
    
global_walking = 0
    
# Run code at fixed time interval
while True:
  schedule.enter(0.01,1,write_data,("filler",))
  schedule.run()
  schedule.enter(0.01,2,read_joystick,("stick",))
  schedule.run()  
  
  if row_count > 100 and enable_data_logging == 1:
    fout = open(filename, 'a')
    for data in list_data:
      fout.write(data + '\n')  
  
    fout.close()      
    list_data = []
  