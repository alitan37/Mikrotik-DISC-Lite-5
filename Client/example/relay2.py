#!/usr/bin/env python

import os
import sys

if not os.getegid() == 0:
	sys.exit('Script must be run as root')


from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

led = port.PA10
buton0 = port.PA20

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)
gpio.setcfg(buton, gpio.INPUT)
gpio.pullup(buton, gpio.PULLUP)

try:
    buton_press=1
    status = 0	
    print ("Press CTRL+C to exit")
    while True:
	buton_press = gpio.input(buton)
  	if (buton_press == 0):
    	   print("Button Pressed")
           gpio.output(led, status)
           sleep(0.5)
           status = ~status
           #gpio.output(led, 0)
           #sleep(0.5)
           # gpio.output(led2, 0)
           # sleep(0.6)

except KeyboardInterrupt:
    	gpio.output(led,1)
	print ("Goodbye.")
