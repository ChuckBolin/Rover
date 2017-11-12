
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED
import sched, time
from time import sleep

sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

red = [120, 0, 0]
green = [0, 120, 0]
sense.clear()


def show_standing(color):
  sense.clear()
  sense.set_pixel(3, 3, color)
  sense.set_pixel(3, 4, color)
  sense.set_pixel(4, 3, color)
  sense.set_pixel(4, 4, color)
  
def show_walking(color):
  sense.clear()
  sense.set_pixel(3, 2, color)
  sense.set_pixel(3, 3, color)
  sense.set_pixel(3, 4, color)
  sense.set_pixel(3, 5, color)
  
def show_spin_right(color):
  sense.clear()
  sense.set_pixel(5, 2, color)
  sense.set_pixel(4, 2, color)
  sense.set_pixel(3, 2, color)
  sense.set_pixel(3, 3, color)
  sense.set_pixel(3, 4, color)
  sense.set_pixel(3, 5, color)
  
def show_spin_left(color):
  sense.clear()
  sense.set_pixel(2, 5, color)
  sense.set_pixel(2, 4, color)
  sense.set_pixel(2, 3, color)
  sense.set_pixel(3, 3, color)
  sense.set_pixel(4, 3, color)
  sense.set_pixel(5, 3, color)
  
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
  #global standing
  #global X
  #global O

  for event in sense.stick.get_events():
    if event.action == ACTION_HELD and event.direction == "middle":
      sense.clear()
    
    # stop data logging
    if event.action == ACTION_RELEASED and event.direction == "down":  
      print ("down")
      #sense.flip_v()
      update_display("go_up", green)

    elif event.action == ACTION_RELEASED and event.direction == "up":  
      print ("up")
      update_display("go_up", red)
      
    elif event.action == ACTION_RELEASED and event.direction == "left":  
      print ("left")
      #update_display("spin_left", red)
      update_display("go_down", green)
    
    elif event.action == ACTION_RELEASED and event.direction == "right":  
      print ("right")
      #update_display("spin_right", red)
      update_display("go_down", red)

 
  
while True:
  schedule.enter(0.25,1,read_joystick,("stick",))
  schedule.run()  
      
  #if walking == 1:
  #  print ("Walking")
  #else:
  #  print ("Stopped")
  #print("The joystick was {} {}".format(event.action, event.direction))
  sleep(0.1)
  event = sense.stick.wait_for_event(emptybuffer=True)

  