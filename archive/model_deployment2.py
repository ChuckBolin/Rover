# Libraries
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED
import sched, time
from time import sleep
from datetime import datetime
import csv
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import Pipeline

import pandas as pd
import numpy as np
import pickle

# Configure Sense Hat and Scheduler
sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep) 

# Global variables
# outside
neutral = [0, 180, 0]
red = [120, 0, 0]
green = [0, 255, 0]
border = [0, 180, 180]

sense.clear()
# data_logging_state = 0
# data_collection_enabled = 0
list_data = []
row_count = 0  
exit_program = 0
global_counter = 0

# Build filename
now = datetime.now()
date_string = now.strftime("%m_%d_%Y")
time_string = now.strftime("%H_%M_%S")
# filename = "data/sensor_" + date_string + "_" + time_string + ".csv"

# Load model using SKlearn
# ========================
model_filename = "model/sensor_model_2017.11.20c.sav"
loaded_model = pickle.load(open(model_filename, 'rb'))
scaler = StandardScaler()

# prediction = loaded_model.predict(scaler.transform(X_test.iloc[i,:].reshape(1,-1))) 
    # print (prediction)
    
# Map function to a list,  map(fx,result)
fx = lambda x: ('%.3f' % float(x))    
sensor_readings_list = [] # stores most recent sensor readings
k = 6 # number of samples to store in temp
result = [] # average of 

def get_model_results(name):
  
  res = get_measurements() # get numpy array with averaged sensor readings
  # print type(res), res.shape
  # print res
  try:
    prediction = loaded_model.predict(scaler.transform(res))  
    print prediction
    update_display(prediction, green)
  except Exception as e:
    print str(e)
    #pass
    
# Param1: state (as text) (e.g. "walking")
# Param2: color, any tuple (e.g. red and green)
# Output: sets pixels for icon
def update_display(state, color):
  
  # global data_collection_enabled
  # global list_data
  # global border
  
  # Clear LED matrix
  sense.clear()
  
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

    
  
  
# Gets measurements
# Returns dataframe
def get_measurements():
  result = [] # average of 
  numpy_array = np.empty([1,15])
  
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
  
  # Combine all of current parameters into a list
  sensor_input_list = [temperature, humidity, pressure, yaw, pitch, roll, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]

  # Need moving average based upon k samples
  # Add this reading to list
  if len(sensor_readings_list) < k:
      sensor_readings_list.append(sensor_input_list)

  # Calculate moving aveage
  if len(sensor_readings_list) == k:

      # result stores the moving average of all sensors
      for j in xrange(len(sensor_readings_list[0])):
          result.append((float(sensor_readings_list[0][j])+float(sensor_readings_list[1][j])+float(sensor_readings_list[2][j]))/k)
      
      # sensor readings list are strings, retain string format for loop
      mydata = sensor_readings_list 
      for i in range(0, len(mydata)):
        mydata[i] = map(float, mydata[i])

      # convert to Pandas dataframe, and get mean values into series
      mydata = pd.DataFrame(mydata) # DF
      scaler.fit(mydata)
      series_result = mydata.mean(axis=0)
      numpy_array = series_result.reshape(1,-1)

  # Remove first sensor reading in list
  if len(sensor_readings_list) >= k:
      del sensor_readings_list[0]
    

  return numpy_array
  
  
# Main loop  

while True:
  # update_display("spin_left", green)
  
  schedule.enter(0.05,1,get_model_results,("predict",))
  schedule.run() 
  
  # Schedule joystick reading every second
  # schedule.enter(0.05,1,write_data,("record",))
  # schedule.run()  
  # schedule.enter(0.05,2,read_joystick,("stick",))
  # schedule.run()  
  

    
exit()

# *********************************************** END OF CODE
# Archive code follows
   
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


  
# Param1: state (as text) (e.g. "walking")
# Param2: color, any tuple (e.g. red and green)
# Output: sets pixels for icon
def update_display(state, color):
  
  # global data_collection_enabled
  # global list_data
  # global border
  
  # Clear LED matrix
  sense.clear()
  
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
  
# Writes data to screen
def write_data(name):

  global list_data
  global row_count
  global data_logging_state
  
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
  
  
  parameters = [date_time_string, temperature, humidity, pressure, yaw, pitch, roll,
  mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, state_text]
  
  output = ','.join(str(x) for x in parameters) #sep.join(parameters)
  row_count += 1
  #print (output)
  
  # Append data
  list_data.append(output)
  return  
  

    
    