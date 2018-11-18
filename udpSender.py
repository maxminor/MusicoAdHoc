# import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 5000
MESSAGE = "HEY"



# sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

from socket import *
import time

# print "UDP target IP:", UDP_IP
# print "UDP target port:", UDP_PORT
# print "message:", MESSAGE

def sendUDPPacket(ip, port, message):

    print('sending {message} to ip:{ip}, port:{port}'.format(**vars()))
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    cs.sendto(message.encode('utf-8'), (ip, port))
# i = 1
# while True:
#     print "sending message: ", i
#     i+=1
#     cs.sendto(MESSAGE, (UDP_IP, UDP_PORT))
#     time.sleep(1)

