#!/usr/bin/env python

import os,sys,socket

if not os.getegid() == 0:
	sys.exit('Script must be run as root')

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

TCP_PORT1 = 3737
BUFFER_SIZE = 20

liveLed = port.PG9
role1 = port.PA10
serLed = port.PA20

def init():
    gpio.init()
    gpio.setcfg(role1, gpio.OUTPUT)
    gpio.setcfg(serLed, gpio.OUTPUT)
    gpio.setcfg(liveLed, gpio.OUTPUT)
    gpio.output(role1, gpio.HIGH) #role kapali
    gpio.output(serLed, gpio.LOW)
    gpio.output(liveLed, gpio.LOW)

init()
for x in range(1, 10):
	gpio.output(serLed, gpio.HIGH)
	sleep(0.2)
	gpio.output(serLed, gpio.LOW)
	sleep(0.2)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT1))
s.listen(1)

conn, addr = s.accept()
print "Connection address:", addr
gpio.output(serLed, gpio.HIGH)
try:
      liveLedDurum = False
      gpio.output(role1, gpio.HIGH)
      while True:
  	   data = conn.recv(BUFFER_SIZE)
           if not data:
            	print 'conection closed'
            	break
                conn.close()
            	#break
           else:
                liveLedDurum = not liveLedDurum
		print data
		gpio.output(liveLed, liveLedDurum)
           if (data == 'AC'):
                gpio.output(role1, gpio.LOW) #Role acik
                #liveLedDurum = not liveLedDurum
		#gpio.output(liveLed, liveLedDurum)
           if (data == 'KAPA'):
                gpio.output(role1, gpio.HIGH) #Role Kapali
                #liveLedDurum = not liveLedDurum
                #gpio.output(liveLed, liveLedDurum)
	   conn.send(data) #echo
except socket.error or KeyboardInterrupt:
       print ("Goodbye.")
finally:
   gpio.output(serLed,gpio.LOW)
   gpio.output(role1, gpio.HIGH) #role kapali
   conn.close();
   s.close();
