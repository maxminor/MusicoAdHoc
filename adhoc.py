import socket 
import json

import udpSender
import heapq

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
class UDPAdHoc:
    def __init__(self, ip, port):
        self.network_name = ''
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
                command = cleaned_data[0:2]
                if command == 'ADD':
                    new_song = cleaned_data[4:]
                    if new_song in self.song_data.keys():
                        self.song_data[str(cleaned_data)] += 1
                    else:
                        self.song_data[str(cleaned_data)] = 1
                elif command == 'LST':
                    if (addr != socket.gethostbyname() and self.network_name != ''):
                        newdata = {'network_name': self.network_name, 'song_data': self.song_data}
                        payload = 'SLS' + json.dumps(newdata)
                        udpSender.sendUDPPacket(addr, 5000, payload.encode('utf-8'))
                elif cleaned_data.split()[0] == 'SLS':
                    received_payload = cleaned_data[4:]
                    newdict = json.loads(received_payload)
                    self.network_name = newdict['network_name']
                    self.data = newdict['song_data']

                # for song in self.song_data.keys():
                #     print("{}: {}".format(str(song), self.song_data[song]))

    def addSong(self, song: str):
        if song in self.song_data:
            self.song_data[song] += 1
        else:
            self.song_data[song] = 1

    def getTopMusic(self, NoOfTopSongs: int):
        return heapq.nlargest(NoOfTopSongs,self.song_data.items(),lambda x: x[1])
