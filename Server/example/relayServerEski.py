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

role4 = port.PA7
role3 = port.PA8
role2 = port.PA9
role1 = port.PA10
serLed = port.PA20

def init():
    gpio.init()
    gpio.setcfg(role1, gpio.OUTPUT)
    gpio.setcfg(role2, gpio.OUTPUT)
    gpio.setcfg(role3, gpio.OUTPUT)
    gpio.setcfg(role4, gpio.OUTPUT)
    gpio.setcfg(serLed, gpio.OUTPUT)
    gpio.output(role1, gpio.HIGH) #role kapali
    gpio.output(role2, gpio.HIGH)
    gpio.output(role3, gpio.HIGH)
    gpio.output(role4, gpio.HIGH)
    gpio.output(serLed, gpio.LOW)
    #gpio.pullup(buton, gpio.PULLUP)

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
      status1 = False
      status2 = False
      status3 = False
      status4 = False
      while True:
	   data = conn.recv(BUFFER_SIZE)
           if not data:
            	print 'conection closed'
            	conn.close()
            	break
           print data
           conn.send(data)
	   if (data == '1'):
                gpio.output(role1, status1)
		status1 = not status1
		data = data +' '+str(status1)
                #print gpio.setcfg(role1, gpio.IN)
           if (data == '2'):
                gpio.output(role2, status2)
                status2 = not status2
	   if (data == '3'):
                gpio.output(role3, status3)
                status3 = not status3
           if (data == '4'):
                gpio.output(role4, status4)
                status4 = not status4
           conn.send(data) #echo

except socket.error or KeyboardInterrupt:
       print ("Goodbye.")
finally:
   gpio.output(serLed,gpio.LOW)
   gpio.output(role1, gpio.HIGH) #role kapali
   gpio.output(role2, gpio.HIGH)
   gpio.output(role3, gpio.HIGH)
   gpio.output(role4, gpio.HIGH)
   gpio.output(serLed, gpio.LOW)
   conn.close();
   s.close();
