#!/usr/bin/env python
import socket,sys,os
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

if not os.getegid() == 0:
	sys.exit('Script must be run as root')

statusled = port.PA13
led1 = port.PA14
led2 = port.PA6
led3 = port.PA1
led4 = port.PA0
buton1 = port.PG7
buton2 = port.PG6
buton3 = port.PG9
buton4 = port.PG8

gpio.init()
gpio.setcfg(led1, gpio.OUTPUT)
gpio.setcfg(led2, gpio.OUTPUT)
gpio.setcfg(led3, gpio.OUTPUT)
gpio.setcfg(led4, gpio.OUTPUT)
gpio.setcfg(statusled, gpio.OUTPUT)
gpio.setcfg(buton1, gpio.INPUT)
gpio.pullup(buton1, gpio.PULLUP)
gpio.setcfg(buton2, gpio.INPUT)
gpio.pullup(buton2, gpio.PULLUP)
gpio.setcfg(buton3, gpio.INPUT)
gpio.pullup(buton3, gpio.PULLUP)
gpio.setcfg(buton4, gpio.INPUT)
gpio.pullup(buton4, gpio.PULLUP)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.2.100', 3737)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    status = True
    led1durum = False
    led2durum = False
    led3durum = False
    led4durum = False
    while True:
        gpio.output(statusled, status)
	sleep(0.25)
	status = not status
        if (gpio.input(buton1)==False) :
            sock.send('1')
            led1durum = not led1durum
            gpio.output(led1, led1durum)
            while (gpio.input(buton1)==False):
		gpio.output(statusled, status)
                sleep(0.25)
		status = not status
	    continue;
        if (gpio.input(buton2)==False) :
            sock.send('2')
            led2durum = not led2durum
            gpio.output(led2, led2durum)
            while (gpio.input(buton2)==False):
		gpio.output(statusled, status)
                sleep(0.25)
		status = not status
	    continue;
        if (gpio.input(buton3)==False) :
            sock.send('3')
            led3durum = not led3durum
            gpio.output(led3, led3durum)
            while (gpio.input(buton3)==False):
		gpio.output(statusled, status)
                sleep(0.25)
		status = not status
	    continue;
        if (gpio.input(buton4)==False) :
            sock.send('4')
            led4durum = not led4durum
            gpio.output(led4, led4durum)
            while (gpio.input(buton4)==False):
		gpio.output(statusled, status)
                sleep(0.25)
		status = not status
	    continue;
        #print(sock.recv(20))
except KeyboardInterrupt:
    sock.close()
