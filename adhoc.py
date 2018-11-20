import socket 
import json
import time

import udpSender
import heapq
import netifaces as ni

import udpSender

# UDP_IP = "0.0.0.0"
# UDP_PORT = 5000
# sock = socket.socket(socket.AF_INET, # Internet
# socket.SOCK_DGRAM) # UDP
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# song_data = {}

#LIST OF COMMANDS
#ADD: add new song to data
#LST: request for new song_data
#SLS: return from LST

import struct
class UDPAdHoc:
    def __init__(self, ip, port):
        self.network_name = 'network1'
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock = socket.socket(socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # timeval = struct.pack('ll',1,0)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)

        self.song_data = {}

        self.waiting_for_SLS_response = False
        self.waiting_start_time = 0
        

    def listenUDP(self):
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print('start listening UDP on port:', self.UDP_PORT)
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            if not data:
                continue
            else: 
                cleaned_data = data.decode('utf-8').strip()
                print("received message:", cleaned_data)
                command = cleaned_data[0:3]
                # print(command)
                if command == 'ADD':
                    new_song = cleaned_data[4:]
                    print(new_song)
                    if new_song in self.song_data.keys():
                        self.song_data[str(new_song)] += 1
                    else:
                        self.song_data[str(new_song)] = 1
                elif command == 'LST':
                    print(addr[0])
                    print(self.network_name)
                    if (addr[0] != self.get_interface_ip() and self.network_name != ''):
                        print('sending new list...')
                        newdata = {'network_name': self.network_name, 'song_data': self.song_data}
                        payload = 'SLS ' + json.dumps(newdata)
                        print(payload)
                        udpSender.sendUDPPacket(str(addr[0]), 5000, payload)

                        
                elif command == 'SLS':
                    print(self.network_name)
                    if(addr != self.get_interface_ip()):
                        received_payload = cleaned_data[4:]
                        print('payload is: ', received_payload)
                        try:
                            newdict = json.loads(received_payload)
                            print(newdict)
                        except e:
                            print(e)
                        self.network_name = newdict['network_name']
                        self.song_data = newdict['song_data']
                        self.stopCountdown()

                # for song in self.song_data.keys():
                #     print("{}: {}".format(str(song), self.song_data[song]))

    def addSong(self, song: str):
        if song in self.song_data:
            self.song_data[song] += 1
        else:
            self.song_data[song] = 1

    def getTopMusic(self, NoOfTopSongs: int):
        return heapq.nlargest(NoOfTopSongs,self.song_data.items(),lambda x: x[1])
    
    def resetData(self):
        self.network_name = ''
        self.song_data = {}

    def requestSLS(self):
        udpSender.sendUDPPacket('10.42.0.255', 5000, 'LST')
        self.waiting_for_SLS_response = True
        self.waiting_start_time = int(time.time())
        print('countdown has been started' , self.waiting_start_time)

    def stopCountdown(self):
        self.waiting_for_SLS_response = False
        # self.waiting_start_time = 0
    
    def countdown(self):
        while True:
            if(self.waiting_for_SLS_response == True):
                if((int(time.time()) - self.waiting_start_time) > 10):
                    self.resetData()
                    print('song and network data has been reset')
                    self.stopCountdown()
                    break
                else:
                    continue
            else:
                print('countdown stopped')
                break
    
    def get_interface_ip(self):
        return str(ni.ifaddresses(ni.interfaces()[-1])[ni.AF_INET][0]['addr'])