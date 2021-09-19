from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep

relay = port.PA10
gpio.init()
gpio.setcfg(relay, gpio.OUTPUT)
gpio.output(relay, gpio.HIGH)
sleep(1)
gpio.output(relay, gpio.LOW)
