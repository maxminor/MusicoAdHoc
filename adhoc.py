import socket 
import json

import udpSender
import heapq

# UDP_IP = "0.0.0.0"
# UDP_PORT = 5000
# sock = socket.socket(socket.AF_INET, # Internet
# socket.SOCK_DGRAM) # UDP
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# song_data = {}


class UDPAdHoc:
    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock = socket.socket(socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.song_data = {}

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
                if cleaned_data.split()[0] not in ['ADD','LIST']:
                    if cleaned_data in self.song_data:
                        self.song_data[str(cleaned_data)] += 1
                    else:
                        self.song_data[str(cleaned_data)] = 1
                # for song in self.song_data.keys():
                #     print("{}: {}".format(str(song), self.song_data[song]))

    def addSong(self, song: str):
        if song in self.song_data:
            self.song_data[song] += 1
        else:
            self.song_data[song] = 1

    def getTopMusic(self, NoOfTopSongs: int):
        return heapq.nlargest(NoOfTopSongs,self.song_data.items(),lambda x: x[1])
