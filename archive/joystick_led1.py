
from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED
import sched, time
from time import sleep

sense = SenseHat()
schedule = sched.scheduler(time.time, time.sleep)

global_walking = 0

# set LED matrix
X = [0, 155, 0]  # Red
O = [20, 20, 160]  # White

question_mark = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, O, O, O, O, X, O, O,
O, O, O, O, X, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, O, O, O, O
]
question_mark2 = [
X, X, X, X, X, X, X, X,
O, O, X, O, O, X, O, O,
O, O, O, O, O, X, O, O,
O, O, O, O, X, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, O, O, O, O
]

#sense.set_pixels(question_mark2)
# examples using (x, y, r, g, b)
sense.clear()
sense.set_pixel(0, 0, 255, 0, 0)
sense.set_pixel(0, 7, 0, 255, 0)
sense.set_pixel(7, 0, 0, 0, 255)
sense.set_pixel(7, 7, 255, 0, 255)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# examples using (x, y, pixel)
sense.set_pixel(0, 0, red)
sense.set_pixel(0, 0, green)
sense.set_pixel(0, 0, blue)


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
    if event.action == ACTION_RELEASED and event.direction == "down":  
      print ("down")
      sense.flip_v()
    elif event.action == ACTION_RELEASED and event.direction == "up":  
      print ("up")
      sense.flip_v()
    elif event.action == ACTION_RELEASED and event.direction == "left":  
      print ("left")
      sense.flip_h()
    elif event.action == ACTION_RELEASED and event.direction == "right":  
      print ("right")  
      sense.flip_h()

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

  