# Libraries
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED
import sched, time
from time import sleep

# Configure Sense Hat and Scheduler
sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

# Global variables
neutral = [0, 60, 0]
red = [120, 0, 0]
green = [0, 180, 0]
sense.clear()
data_logging_state = 0
data_collection_enabled = 0
  
  
# Param1: state (as text) (e.g. "walking")
# Param2: color, any tuple (e.g. red and green)
# Output: sets pixels for icon
def update_display(state, color):

  # Clear LED matrix
  sense.clear()
  
  # Render various states
  if state == "walking":
      sense.set_pixel(3, 2, color)
      sense.set_pixel(3, 3, color)
      sense.set_pixel(3, 4, color)
      sense.set_pixel(3, 5, color)
  elif state == "standing":
      sense.set_pixel(3, 3, color)
      sense.set_pixel(3, 4, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(4, 4, color)
  elif state == "spin_left":
      sense.set_pixel(2, 5, color)
      sense.set_pixel(2, 4, color)
      sense.set_pixel(2, 3, color)
      sense.set_pixel(3, 3, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(5, 3, color)
  elif state == "spin_right":
      sense.set_pixel(2, 5, color)
      sense.set_pixel(2, 4, color)
      sense.set_pixel(2, 3, color)
      sense.set_pixel(3, 3, color)
      sense.set_pixel(4, 3, color)
      sense.set_pixel(5, 3, color)
      sense.flip_h()
  elif state == "go_up":
      sense.set_pixel(3,5, color)
      sense.set_pixel(4,5, color)
      sense.set_pixel(5,5, color)
      sense.set_pixel(6,5, color)
      sense.set_pixel(4,4, color)
      sense.set_pixel(5,3, color)
      sense.set_pixel(6,2, color)
  elif state == "go_down":
      sense.set_pixel(3,5, color)
      sense.set_pixel(4,5, color)
      sense.set_pixel(5,5, color)
      sense.set_pixel(6,5, color)
      sense.set_pixel(4,4, color)
      sense.set_pixel(5,3, color)
      sense.set_pixel(6,2, color)
      sense.flip_v()

#  Param: Dummy variable required for schedule function call      
def read_joystick(name):

  # global scope
  global red
  global green
  global data_logging_state
  global data_collection_enabled
  
  # loop through events, usually single event
  for event in sense.stick.get_events():
  
    # Middle button press to toggle data collection
    if event.action == ACTION_PRESSED and event.direction == "middle":
      if data_collection_enabled == 0:
        data_collection_enabled = 1
      else:
        data_collection_enabled = 0 # stop data logging

    # Change states from 0 to 5  
    if event.action == ACTION_PRESSED and event.direction == "up":  
      data_logging_state += 1
      if data_logging_state > 5:
        data_logging_state = 0    
    elif event.action == ACTION_PRESSED and event.direction == "down":  
      data_logging_state -= 1
      if data_logging_state < 0:
        data_logging_state = 5
      
# Main loop  
while True:

  # Schedule joystick reading every second
  schedule.enter(1,1,read_joystick,("stick",))
  schedule.run()  
  
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
    
  # Display states
  print data_collection_enabled, data_logging_state
  
  