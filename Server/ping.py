import os

def pingat():
    hostname = "192.168.2.99" #example
    #response = os.system("ping -c 1 " + hostname)
    response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
    #and then check the response...
    if response == 0:
       #print hostname, 'is up!'
       return True
    else:
       #print hostname, 'is down!'
       return False

try:
    while True:
         if pingat():
   	     pass #print("Canli")
         else:
             print("Reboot")
             os.system("sudo reboot > restart.log &")
except KeyboardInterrupt:
       print "keyb"
finally:
       print "bye"
