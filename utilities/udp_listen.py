#!/usr/bin/python

import sys
import socket
import time
import signal

terminate = False                            

def signal_handling(signum,frame):           
    global terminate                         
    terminate = True

#---socket creation
connexion = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if sys.platform != "win32":
    connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

#---Bind
try:
    connexion.bind(('', int(sys.argv[1])))
except socket.error:
    print ("connexion failed")
    connexion.close()
    sys.exit()

signal.signal(signal.SIGINT,signal_handling) 
fd = open(sys.argv[2], "w+")
connexion.setblocking(0)

#---wait for and print data
while 1:
    try:
        if terminate:
            print("Exiting..")
            fd.close()   
            sys.exit()
        data, addr = connexion.recvfrom(1024)
        towrite = data.decode("utf-8") + "\n"
        print(time.time(), ":", data.decode("utf-8"))
        fd.write(towrite)
    except BlockingIOError:
        pass