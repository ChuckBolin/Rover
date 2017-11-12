
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED
import sched, time
from time import sleep

sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

walking = 0


# set LED matrix



#sense.set_pixels(question_mark2)
# examples using (x, y, r, g, b)
sense.clear()
#sense.set_pixels(standing)



def read_joystick(name):
  global walking
  #global standing
  #global X
  #global O

  for event in sense.stick.get_events():
    if event.action == ACTION_HELD and event.direction == "middle":
      walking = 1
      #print ("Walking")
    else:
      walking = 0
      #print ("Stopped")
    
    # stop data logging
    if event.action == ACTION_RELEASED and event.direction == "down":  
      print ("down")
      #sense.flip_v()
      sense.clear()
      X = [120, 0, 0]
      O = [0, 0, 0]
      standing = [
      O, O, O, O, O, O, O, O,
      O, X, O, O, O, O, X, O,
      O, O, X, O, O, X, O, O,
      O, O, O, X, X, O, O, O,
      O, O, O, X, X, O, O, O,
      O, O, X, O, O, X, O, O,
      O, X, O, O, O, O, X, O,
      O, O, O, O, O, O, O, O
      ]      
      sense.set_pixels(standing)

    elif event.action == ACTION_RELEASED and event.direction == "up":  
      print ("up")
      #sense.flip_v()
      sense.clear()
      X = [0, 120, 0]
      O = [0, 0, 0]
      standing = [
      O, O, O, O, O, O, O, O,
      O, X, O, O, O, O, X, O,
      O, O, X, O, O, X, O, O,
      O, O, O, X, X, O, O, O,
      O, O, O, X, X, O, O, O,
      O, O, X, O, O, X, O, O,
      O, X, O, O, O, O, X, O,
      O, O, O, O, O, O, O, O
      ]
      sense.set_pixels(standing)

    #elif event.action == ACTION_RELEASED and event.direction == "left":  
    #  print ("left")
    #  sense.flip_h()
    #elif event.action == ACTION_RELEASED and event.direction == "right":  
    #  print ("right")  
    #  sense.flip_h()  
  
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

  