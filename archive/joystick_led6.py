
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED
import sched, time
from time import sleep

sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

red = [120, 0, 0]
green = [0, 120, 0]
sense.clear()
data_logging_state = 0
data_collection_enabled = 0
  
def update_display(state, color):
  sense.clear()
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

def read_joystick(name):
  global red
  global green
  global data_logging_state
  global data_collection_enabled
  
  for event in sense.stick.get_events():
    if event.action == ACTION_PRESSED and event.direction == "middle":
      if data_collection_enabled == 0:
        data_collection_enabled = 1
      else:
        data_collection_enabled = 0 # stop data logging

      
    
    if event.action == ACTION_PRESSED and event.direction == "down":  

      data_logging_state -= 1
      if data_logging_state < 0:
        data_logging_state = 5

    elif event.action == ACTION_PRESSED and event.direction == "up":  
      data_logging_state += 1
      if data_logging_state > 5:
        data_logging_state = 0



      
      
  
while True:
  schedule.enter(1,1,read_joystick,("stick",))
  schedule.run()  
  
  if data_logging_state == 0:
    update_display("standing", red)
  elif data_logging_state == 1:
    update_display("walking", red)
  elif data_logging_state == 2:
    update_display("spin_left", red)
  elif data_logging_state == 3:
    update_display("spin_right", red)
  elif data_logging_state == 4:
    update_display("go_up", red)
  elif data_logging_state == 5:
    update_display("go_down", red)
  
  print data_collection_enabled, data_logging_state
  
  