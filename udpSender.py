# import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 5000
MESSAGE = "HEY"



# sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

from socket import *
import time

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
i = 1
while True:
    print "sending message: ", i
    i+=1
    cs.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(1)

