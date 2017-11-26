# from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED, ACTION_PRESSED

# Configure Sense Hat and Scheduler
# sense = SenseHat()



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