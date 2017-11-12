from sense_hat import SenseHat, ACTION_HELD
from time import sleep

sense = SenseHat()
walking = 0
while True:
  
  # wait for event
  event = sense.stick.wait_for_event()
  
  # print 1
  if event.action == ACTION_HELD and event.direction == "middle":
    walking = 1
  else:
    walking = 0

  # stop data logging
  if event.action == ACTION_HELD and event.direction == "down":  
    break

  if walking == 1:
    print ("Walking")
  else:
    print ("Stopped")
  #print("The joystick was {} {}".format(event.action, event.direction))
  sleep(0.1)
  event = sense.stick.wait_for_event(emptybuffer=True)
