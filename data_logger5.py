# requires tis bash command
# sudo gpsd -F /var/run/gpsd.sock /dev/ttyUSB0

# Libraries
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED
import sched #, time
from time import sleep
from datetime import datetime
import csv

import os 
from gps import *
from time import *
import time 
import threading 
from gps_poll import *

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
    # gps_available = 1
        
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
header = 'DateTime, Latitude, Longitude, Temp, Humidity, Pressure, Yaw, Pitch, Roll, MagX, MagY, MagZ, AccX, AccY, AccZ, GyroX, GyroY, GyroZ, State'  
list_data.append(header)
latitude = ''
longitude = ''


            
# Writes data to screen
def write_data(name):

  global list_data
  global row_count
  global data_logging_state
  global latitude
  global longitude
  global gps_available
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
      latitude = report['lat']
      longitude = report['lon']    
      gps_available = 1
  except(AttributeError, KeyError):
    gps_available = 0
    pass 
                
  
  # Construct formatted output
  # Get state text for numerical state
  state_text = ''
  if data_logging_state == 0:
    state_text = "standing"
  elif data_logging_state == 1:
    state_text = "walking"
  elif data_logging_state == 2:
    state_text = "spin_left"
  elif data_logging_state == 3:
    state_text = "spin_right"
  elif data_logging_state == 4:
    state_text = "go_up"
  elif data_logging_state == 5:
    state_text = "go_down"  
  elif data_logging_state == 6:
    state_text = "turn_left"  
  elif data_logging_state == 7:
    state_text = "turn_right"  
  
  
  
  parameters = [date_time_string, latitude, longitude, temperature, humidity, pressure, yaw, pitch, roll, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, state_text]
  
  output = ','.join(str(x) for x in parameters) #sep.join(parameters)
  row_count += 1
  #print (output)
  
  # Append data
  list_data.append(output)
  return  
  
def show_count():
  global global_counter
  step = 1
  if global_counter >= step * 1:
    sense.set_pixel(0, 7, border)
  if global_counter >=  step * 2:
    sense.set_pixel(0, 6, border)
  if global_counter >=  step * 3:
    sense.set_pixel(0, 5, border)
  if global_counter >=  step * 4:
    sense.set_pixel(0, 4, border)
  if global_counter >=  step * 5:
    sense.set_pixel(0, 3, border)
  if global_counter >=  step * 6:
    sense.set_pixel(0, 2, border)
  if global_counter >=  step * 7:
    sense.set_pixel(0, 1, border)
  if global_counter >=  step * 8:
    sense.set_pixel(0, 0, border)

  if global_counter >=  step * 9:
    sense.set_pixel(1, 0, border)
  if global_counter >=  step * 10:
    sense.set_pixel(2, 0, border)
  if global_counter >=  step * 11:
    sense.set_pixel(3, 0, border)
  if global_counter >=  step * 12:
    sense.set_pixel(4, 0, border)
  if global_counter >=  step * 13:
    sense.set_pixel(5, 0, border)
  if global_counter >=  step * 14:
    sense.set_pixel(6, 0, border)
  if global_counter >=  step * 15:
    sense.set_pixel(7, 0, border)
    
  if global_counter >=  step * 16:
    sense.set_pixel(7, 1, border)
  if global_counter >=  step * 17:
    sense.set_pixel(7, 2, border)
  if global_counter >=  step * 18:
    sense.set_pixel(7, 3, border)
  if global_counter >=  step * 19:
    sense.set_pixel(7, 4, border)
  if global_counter >=  step * 20:
    sense.set_pixel(7, 5, border)
  if global_counter >=  step * 21:
    sense.set_pixel(7, 6, border)
  if global_counter >=  step * 22:
    sense.set_pixel(7, 7, border)
    
  if global_counter >=  step * 23:
    sense.set_pixel(6, 7, border)
  if global_counter >=  step * 24:
    sense.set_pixel(5, 7, border)
  if global_counter >=  step * 25:
    sense.set_pixel(4, 7, border)
  if global_counter >=  step * 26:
    sense.set_pixel(3, 7, border)
  if global_counter >=  step * 27:
    sense.set_pixel(2, 7, border)
  if global_counter >=  step * 28:
    sense.set_pixel(1, 7, border)

  if global_counter >=  step * 29:
    global_counter = 0
  
# Param1: state (as text) (e.g. "walking")
# Param2: color, any tuple (e.g. red and green)
# Output: sets pixels for icon
def update_display(state, color):
  
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
  
  
  # Render various states
  if state == "walking":
      sense.set_pixel(3, 2, color)
      sense.set_pixel(3, 3, color)
      sense.set_pixel(3, 4, color)
      sense.set_pixel(3, 5, color)
      sense.set_pixel(4, 2, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(4, 4, color)
      sense.set_pixel(4, 5, color)      
  elif state == "standing":
      sense.set_pixel(3, 3, color)
      sense.set_pixel(3, 4, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(4, 4, color)
  elif state == "spin_left":
      sense.set_pixel(2, 3, color)
      sense.set_pixel(3, 3, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(5, 3, color)
      sense.set_pixel(2, 4, color)
      sense.set_pixel(5, 4, color)
      sense.set_pixel(5, 5, color)
      sense.set_pixel(3, 5, color)
  elif state == "spin_right":
      sense.set_pixel(2, 3, color)
      sense.set_pixel(3, 3, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(5, 3, color)
      sense.set_pixel(2, 4, color)
      sense.set_pixel(5, 4, color)
      sense.set_pixel(5, 5, color)
      sense.set_pixel(3, 5, color)
      sense.flip_h()      
  elif state == "go_up":
      sense.set_pixel(2,5, color)
      sense.set_pixel(3,5, color)
      sense.set_pixel(4,5, color)
      sense.set_pixel(5,5, color)
      sense.set_pixel(3,4, color)
      sense.set_pixel(4,3, color)
      sense.set_pixel(5,2, color)
  elif state == "go_down":
      sense.set_pixel(2,5, color)
      sense.set_pixel(3,5, color)
      sense.set_pixel(4,5, color)
      sense.set_pixel(5,5, color)
      sense.set_pixel(3,4, color)
      sense.set_pixel(4,3, color)
      sense.set_pixel(5,2, color)
      sense.flip_v()
  elif state == "turn_left":
      sense.set_pixel(2,2, color)
      sense.set_pixel(3,2, color)
      sense.set_pixel(4,3, color)
      sense.set_pixel(5,4, color)
      sense.set_pixel(5,5, color)
  elif state == "turn_right":
      sense.set_pixel(2,2, color)
      sense.set_pixel(3,2, color)
      sense.set_pixel(4,3, color)
      sense.set_pixel(5,4, color)
      sense.set_pixel(5,5, color)
      sense.flip_h()

      
  show_count()
    
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
    
    
  # Render LED display icons
  # No data collection
  if data_logging_state == 0 and data_collection_enabled == 0:
    update_display("standing", neutral)
  elif data_logging_state == 1 and data_collection_enabled == 0:
    update_display("walking", neutral)
  elif data_logging_state == 2 and data_collection_enabled == 0:
    update_display("spin_left", neutral)
  elif data_logging_state == 3 and data_collection_enabled == 0:
    update_display("spin_right", neutral)
  elif data_logging_state == 4 and data_collection_enabled == 0:
    update_display("go_up", neutral)
  elif data_logging_state == 5 and data_collection_enabled == 0:
    update_display("go_down", neutral)
  elif data_logging_state == 6 and data_collection_enabled == 0:
    update_display("turn_left", neutral)
  elif data_logging_state == 7 and data_collection_enabled == 0:
    update_display("turn_right", neutral)
    
  # Data collection
  elif data_logging_state == 0 and data_collection_enabled == 1:
    update_display("standing", green)
  elif data_logging_state == 1 and data_collection_enabled == 1:
    update_display("walking", green)
  elif data_logging_state == 2 and data_collection_enabled == 1:
    update_display("spin_left", green)
  elif data_logging_state == 3 and data_collection_enabled == 1:
    update_display("spin_right", green)
  elif data_logging_state == 4 and data_collection_enabled == 1:
    update_display("go_up", green)
  elif data_logging_state == 5 and data_collection_enabled == 1:
    update_display("go_down", green)
  elif data_logging_state == 6 and data_collection_enabled == 1:
    update_display("turn_left", green)
  elif data_logging_state == 7 and data_collection_enabled == 1:
    update_display("turn_right", green)
    
  # Display states
  # print data_collection_enabled, data_logging_state, global_counter
  
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
    
    
    