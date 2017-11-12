from sense_hat import SenseHat, ACTION_HELD
import sched, time
from time import sleep

sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

global_walking = 0

def read_joystick(name):
  walking = 0
  for event in sense.stick.get_events():
    if event.action == ACTION_HELD and event.direction == "middle":
      walking = 1
    else:
      walking = 0

    if walking == 1:
      print ("Walking")
    else:
      print ("Stopped")
    
    # stop data logging
    if event.action == ACTION_HELD and event.direction == "down":  
      print ("down")
    elif event.action == ACTION_HELD and event.direction == "up":  
      print ("up")
    elif event.action == ACTION_HELD and event.direction == "left":  
      print ("left")
    elif event.action == ACTION_HELD and event.direction == "right":  
      print ("right")  

  global_walking = walking
  
while True:
  schedule.enter(0.25,1,read_joystick,("stick",))
  schedule.run()  
  
  if global_walking == 1:
    print ("Walking")
  else:
    print ("Stopped")
  
  
def archive():
  # wait for event
  event = sense.stick.wait_for_event()
  
  # print 1
  if event.action == ACTION_HELD and event.direction == "middle":
    walking = 1
  else:
    walking = 0

  # stop data logging
  if event.action == ACTION_HELD and event.direction == "down":  
    print ("down")
  elif event.action == ACTION_HELD and event.direction == "up":  
    print ("up")
  elif event.action == ACTION_HELD and event.direction == "left":  
    print ("left")
  elif event.action == ACTION_HELD and event.direction == "right":  
    print ("right")

    
  if walking == 1:
    print ("Walking")
  else:
    print ("Stopped")
  #print("The joystick was {} {}".format(event.action, event.direction))
  sleep(0.1)
  event = sense.stick.wait_for_event(emptybuffer=True)

  