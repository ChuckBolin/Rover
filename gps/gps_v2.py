#!/usr/bin/python
import os, sys
import pygame
# from pygame.locals import *
import serial

#initialise serial port on /ttyUSB0
# ls /dev/tty* Compare without GPS connect to it connected,
# difference is ttyUSB0
ser = serial.Serial('/dev/ttyUSB0',4800,timeout = None)
fix = 1
x = 0
while x == 0:
   gps = ser.readline()
   fix = 1
   
   # print all NMEA strings
   print gps #[1:6]   
   
   # check gps fix status
   # if gps[1:6] == "GPGSA":
      # fix = int(gps[9:10])
      
   # print time, lat and long from #GPGGA string
   if gps[1:6] == "GPGGA":
       time = gps[7:9] + ":" + gps[9:11] + ":" + gps[11:13]

       if fix > 1:
          lat = " " + gps[18:20] + "." + gps[20:22] + "." + gps[23:27] + gps[28:29]
          lon = " " + gps[30:33] + "." + gps[33:35] + "." + gps[36:40] + gps[41:42]
       else:
          lat = " No Valid Data "
          lon = " "
       print str(time), str(lat), str(lon)