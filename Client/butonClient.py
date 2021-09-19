#!/usr/bin/env python
import socket,sys,os,random

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

if not os.getegid() == 0:
	sys.exit('Script must be run as root')

statusled = port.PA13
led_dolu = port.PA1
led_bos = port.PA0
#led_alarm = port.PA6
buton_ac = port.PG7
buton_kapa = port.PG6

gpio.init()
gpio.setcfg(led_dolu, gpio.OUTPUT)
gpio.setcfg(led_bos, gpio.OUTPUT)
gpio.setcfg(statusled, gpio.OUTPUT)
gpio.setcfg(buton_ac, gpio.INPUT)
#gpio.setcfg(led_alarm, gpio.OUTPUT)
gpio.pullup(buton_ac, gpio.PULLUP)
gpio.setcfg(buton_kapa, gpio.INPUT)
gpio.pullup(buton_kapa, gpio.PULLUP)
gpio.output(led_dolu, gpio.LOW)
gpio.output(led_bos, gpio.LOW)
gpio.output(statusled,gpio.LOW)
#gpio.output(led_alarm,gpio.LOW)

for x in range(1, 10):
        gpio.output(statusled, gpio.HIGH)
        sleep(0.1)
        gpio.output(statusled, gpio.LOW)
        sleep(0.1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.2.100', 3737)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    status = True
    bosdurum = False
    doludurum = True
    gpio.output(led_bos, bosdurum)
    gpio.output(led_dolu, doludurum)
    while True:
	gpio.output(statusled, status)
	sleep(0.25)
	status = not status
        if (gpio.input(buton_ac)==False) :
            sock.send('AC')
            bosdurum = True
            doludurum = False
            gpio.output(led_bos, bosdurum)
            gpio.output(led_dolu, doludurum)
            while (gpio.input(buton_ac)==False):
		gpio.output(statusled, status)
                sleep(0.25)
		status = not status
                sock.send('AC')
	    continue;
        if (gpio.input(buton_kapa)==False) :
            sock.send('KAPA')
            bosdurum = False
            doludurum = True
            gpio.output(led_bos, bosdurum)
            gpio.output(led_dolu, doludurum)
            alarmdurum = False
            while (gpio.input(buton_kapa)==False):
		gpio.output(statusled, status)
                sleep(0.25)
		status = not status
                sock.send('KAPA')
	    continue;
        rnd = random.randint(1,12)
        sock.send(str(rnd))
	sleep(0.05)
        data = sock.recv(1024)
        print(data.decode())
        #if not data:
except KeyboardInterrupt:
       print "bye"
finally:
   print "bye bye"
   sock.send('KAPA')
   sock.close()
   gpio.output(led_bos, bosdurum)
   gpio.output(led_dolu, doludurum)
   #gpio.output(led_alarm, alarmdurum)
