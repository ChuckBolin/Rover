#https://projects.raspberrypi.org/en/projects/sense-hat-data-logger

from sense_hat import SenseHat
from datetime import datetime
import sched, time

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

def write_data(a):

  now = datetime.now()
  date_time_string = now.strftime("%Y-%m-%d, %H:%M:%S")

  # Color sensor values
  temperature = "{0:.2f}".format(sense.get_temperature()) 
  humidity = "{0:.2f}".format(sense.get_humidity())
  pressure = "{0:.2f}".format(sense.get_pressure())

  # Construct formatted output
  sep = ", "
  print ('Date, Time, Temp, Humidity, Pressure')
  parameters = [date_time_string, temperature, humidity, pressure]
  output = sep.join(parameters)
  
  print (output)

while True:
  schedule.enter(0.5,1,write_data,('params',))
  schedule.run()

        
# Loop forever
#while True:

  # Color sensor values
  #temperature = "{0:.2f}".format(sense.get_temperature()) 
  #humidity = "{0:.2f}".format(sense.get_humidity())
  #pressure = "{0:.2f}".format(sense.get_pressure())

  # Construct formatted output
  #sep = ","
  #parameters = [temperature, humidity, pressure]
  #output = sep.join(parameters)
  #print (output)
  
  
        
        