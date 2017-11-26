# Libraries


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

from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED
# Configure Sense Hat and Scheduler
sense = SenseHat()

from functions.py import  update_display #(state, color)


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
k = 11 # number of samples to store in temp
result = [] # average of 

def get_model_results(name):
  
  res = get_measurements() # get numpy array with averaged sensor readings
  # print type(res), res.shape
  print res
  
  try:
    prediction = loaded_model.predict(scaler.transform(res))  
    # print prediction
    update_display(prediction, border)
  except Exception as e:
    print str(e)
    #pass
    

  
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

  # Remove first sensor reading in list
  if len(sensor_readings_list) >= k:
      del sensor_readings_list[0]    
      
  # Calculate moving aveage
  if len(sensor_readings_list) == k:

      # result stores the moving average of all sensors
      for j in xrange(len(sensor_readings_list[0])):
          result.append((float(sensor_readings_list[0][j])+float(sensor_readings_list[1][j])+float(sensor_readings_list[2][j]))/k)
      
      # sensor readings list are strings, retain string format for loop
      mydata = sensor_readings_list 
      for i in range(0, len(mydata)):
        mydata[i] = map(float, mydata[i])
        # mydata[i] = map(fx, mydata[i])

        
      # convert to Pandas dataframe, and get mean values into series
      mydata = pd.DataFrame(mydata) # DF
      scaler.fit(mydata)
      series_result = mydata.mean(axis=0)
      series_result = pd.Series(map(fx, series_result))
      numpy_array = series_result.reshape(1,-1)
  
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

    
    