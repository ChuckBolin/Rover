# requires tis bash command
# sudo gpsd -F /var/run/gpsd.sock /dev/ttyUSB0

# Libraries
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED
import sched #, time
from time import sleep
from datetime import datetime
import csv
import math
from geographiclib.geodesic import Geodesic
import os 
from gps import *
from time import *
import time 
import threading 
from gps_poll import *
# from multiprocessing import Process

# Configure Sense Hat and Scheduler
sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep) 
        
# Global variables
neutral = [0, 80, 0]
red = [120, 0, 0]
green = [0, 150, 0]
border = [0, 50, 50]
data_logging_state = 0
data_collection_enabled = 0
list_data = []
row_count = 0  
exit_program = 0
global_counter = 0
gps_available = 0

# GPS    
gpsp = GpsPoller()

try: 
    gpsp.start() 
    gps_available = 1
except(KeyboardInterrupt, SystemExit):
    print "\nKilling Thread.."
    gps_available = 0
    gpsp.running = False 
    gpsp.join()

# sensor module
sense.clear()

# Build filename
now = datetime.now()
date_string = now.strftime("%m_%d_%Y")
time_string = now.strftime("%H_%M_%S")
filename = "data/sensor_" + date_string + "_" + time_string + ".csv"

# Write header
header = 'DateTime, Latitude, Longitude, Temp, Humidity, Pressure, Yaw, Pitch, Roll, MagX, MagY, MagZ, AccX, AccY, AccZ, GyroX, GyroY, GyroZ, Velocity, Heading'  
list_data.append(header)
latitude = 0.0
longitude = 0.0
prev_latitude = 0.0
prev_longitude = 0.0
bearing = 0.0
velocity = 0.0
            
# Writes data to screen
def write_data(name):

  global list_data
  global row_count
  global data_logging_state
  global latitude
  global longitude
  global prev_latitude
  global prev_longitude
  global gps_available
  global bearing
  global velocity
  
  if data_collection_enabled == 0:
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
  
  # print report 
  report = gpsp.get_current_value()
  
  try: 
    if report.keys()[0] == 'epx':
      latitude = float(report['lat'])
      longitude = float(report['lon'])
      velocity = float(report['speed'])
      
      pos = Geodesic.WGS84.Inverse(prev_latitude, prev_longitude,latitude,longitude) #-41.32, 174.81, 40.96, -5.50))

      # print(pos) 
      bearing = float(pos['azi1'])
      
      # lat1 = math.radians(prev_latitude)
      # lat2 = math.radians(latitude)
      # lon1 = math.radians(prev_longitude)
      # lon2 = math.radians(longitude)      
      # dLon =lon2 - lon1
      # y = math.sin(dLon) * math.cos(lat2)
      # x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
      # try:
        # bearing = math.atan2(y, x).toDeg()      
      # except:
        # pass
      
      if (bearing < 0):
        bearing+= 360
      
  
      print (latitude, longitude, velocity, bearing)
      
      # print (report['lat'], report['lon'], report['alt'],report['speed'],report['time'], report['mode']) #, report['track'])
      # print (pos['azi2'])
      prev_latitude = latitude
      prev_longitude = longitude
  
  except(AttributeError, KeyError):
    print ("no")
    pass 
                
  
  parameters = [date_time_string, str(latitude), str(longitude), temperature, humidity, pressure, yaw, pitch, roll, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, velocity, bearing]
  
  output = ','.join(str(x) for x in parameters) #sep.join(parameters)
  row_count += 1
  # print (output)
  
  # Append data
  list_data.append(output)
  


  return  

  
# Param1: state (as text) (e.g. "walking")
# Param2: color, any tuple (e.g. red and green)
# Output: sets pixels for icon
def update_display():
  
  global data_collection_enabled
  # global list_data
  global border
  global gps_available
  
  # Clear LED matrix
  sense.clear()
  
  if gps_available == 1:
    sense.set_pixel(1, 1, green)
  else:
    sense.set_pixel(1, 1, red)  

  if data_collection_enabled == 1:
    sense.set_pixel(1, 6, green)
  else:
    sense.set_pixel(1, 6, red)  
    
    
    
#  Param: Dummy variable required for schedule function call      
def read_joystick(name):

  # global scope
  global red
  global green
  global data_logging_state
  global data_collection_enabled
  global exit_program
  
  # loop through events, usually single event
  for event in sense.stick.get_events():
  
    # Middle button press to toggle data collection
    if event.action == ACTION_PRESSED and event.direction == "middle":
      if data_collection_enabled == 0:
        data_collection_enabled = 1
      else:
        data_collection_enabled = 0 # stop data logging

    # Exit program
    if event.action == ACTION_HELD and event.direction == "right":
      exit_program = 1
        
    # Change states from 0 to 5  
    min_state = 0
    max_state = 7
    if event.action == ACTION_PRESSED and event.direction == "up":  
      data_logging_state += 1
      if data_logging_state > 7:# max_state:
        data_logging_state = 0 #min_state    
    elif event.action == ACTION_PRESSED and event.direction == "down":  
      data_logging_state -= 1
      if data_logging_state < 0: #min_state:
        data_logging_state = 7 #max_state
      
# Main loop  

while True:

  # Schedule joystick reading every second
  schedule.enter(0.05,1,write_data,("record",))
  schedule.run()  
  schedule.enter(0.05,2,read_joystick,("stick",))
  schedule.run()  
  
  if row_count > 10 and data_collection_enabled == 1:
    global_counter += 1
  
  if row_count > 50 and data_collection_enabled == 1:
    fout = open(filename, 'a')
    for data in list_data:
      fout.write(data + '\n')    
    fout.close()      
    list_data = []
    row_count = 0
    
  update_display()
  
  # if gpsp.running = True:
    # gps_available = 1
  # else:
    # gps_available = 0
    
  # Housekeeping and then exit
  if exit_program == 1:
    
    if data_collection_enabled == 1:
      fout = open(filename, 'a')
      for data in list_data:
        fout.write(data + '\n')  
      fout.close() 
    
    sense.clear()
    gpsp.running = False 
    gpsp.join()
    exit()
    
    
    