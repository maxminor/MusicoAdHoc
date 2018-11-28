import socket 
import json
import time
import os
import pprint

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
    def __init__(self,network_name, ip, port):
        self.network_name = network_name
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock = socket.socket(socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # self.adHocinterfaces = self.getAdHocIntefaces()

        #dict that store latest sequence if for each senders for ADD command
        # format {'sendername': number}
        self.received_sequence_numbers = {}

        self.add_sequence_count = 0

        self.song_data = {}

        self.waiting_for_SLS_response = False
        self.waiting_start_time = 0
        

    def listenUDP(self):
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print('start listening UDP on port:', self.UDP_PORT)
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            temp = addr[0].split('.')[:-1]
            temp.append('255')
            senderBroadcastAddr = '.'.join(temp)
            if not data:
                continue
            else: 
                cleaned_data = data.decode('utf-8').strip()
                print("received message:", cleaned_data)
                command = cleaned_data[0:3]
                # print(command)
                if command == 'ADD':
                    payload = json.loads(cleaned_data[4:])
                    pp = pprint.PrettyPrinter(indent=4)
                    pp.pprint(payload)
                    #not your own ip
                    #sender not in received_sequence_numbers
                    #if it has, sequence number must be more than current seq number
                    if(self.isOwnIP(addr[0]) == True):
                        print('ADD message rejected, your own message')
                        continue
                    elif(payload['sender'] in self.received_sequence_numbers.keys()):
                        if(payload['sequence_number'] <= self.received_sequence_numbers[payload['sender']]):
                            print('Add message rejected, old seq number')
                            continue

                    #broadcast to other ips
                    #retrieve sender broadcast addr
                    #assume subnet is 24 bit
                    # senderBroadcastAddr = addr[0].split('.').pop().append('255').join('.')
                    # AdHocinterfaces = self.getAdHocIntefaces()
                    print('message is not rejected, sending...')
                    self.addSong(payload['song'])
                    for intf in self.getAdHocIntefaces():
                        broadcastIP = self.getInterfaceBroadcastAddresses(intf)
                        if(broadcastIP != senderBroadcastAddr):
                            udpSender.sendUDPPacket(str(broadcastIP), 5000, cleaned_data)


                elif command == 'LST':
                    print(addr[0])
                    print(self.network_name)
                    if ((self.isOwnIP() == False) and self.network_name != ''):
                        print('sending new list...')
                        newdata = {'network_name': self.network_name, 'song_data': self.song_data}
                        payload = 'SLS ' + json.dumps(newdata)
                        print(payload)
                        udpSender.sendUDPPacket(str(addr[0]), 5000, payload)

                        
                elif command == 'SLS':
                    print(self.network_name)
                    if((self.isOwnIP() == False)):
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
        if song in self.song_data.keys():
            self.song_data[song] += 1
        else:
            self.song_data[song] = 1

    def getTopMusic(self, NoOfTopSongs: int):
        return heapq.nlargest(NoOfTopSongs,self.song_data.items(),lambda x: x[1])
    
    def resetData(self):
        self.network_name = ''
        self.song_data = {}

    def requestSLS(self):
        adhocintf = self.getAdHocIntefaces()
        for intf in adhocintf:
            udpSender.sendUDPPacket(intf, 5000, 'LST')
        # udpSender.sendUDPPacket('10.42.0.255', 5000, 'LST')
        # self.waiting_for_SLS_response = True
        # self.waiting_start_time = int(time.time())
        # print('countdown has been started' , self.waiting_start_time)

    def stopCountdown(self):
        self.waiting_for_SLS_response = False
        # self.waiting_start_time = 0
    
    # def countdown(self):
    #     while True:
    #         if(self.waiting_for_SLS_response == True):
    #             if((int(time.time()) - self.waiting_start_time) > 10):
    #                 self.resetData()
    #                 print('song and network data has been reset')
    #                 self.stopCountdown()
    #                 break
    #             else:
    #                 continue
    #         else:
    #             print('countdown stopped')
    #             break

    def getAdHocIntefaces(self):
        interfaces = ni.interfaces()
        ahintf = []
        for intf in interfaces:
            if(intf[0:2] == 'wl'):
                command = 'iwconfig ' + intf + " | grep 'Mode:'"
                if (os.popen(command).read().strip().split()[0].split(':')[1] == 'Ad-Hoc'):
                    ahintf.append(intf)
        return ahintf
    
    def getInterfaceBroadcastAddresses(self, intf: str):
        return str(ni.ifaddresses(intf)[ni.AF_INET][0]['broadcast'])
    
    def isOwnIP(self, addr: str):
        for intf in self.getAdHocIntefaces():
            if(addr == self.get_interface_ip(intf)):
                return True
        return False

    def get_interface_ip(self, intf: str):
        return str(ni.ifaddresses(intf)[ni.AF_INET][0]['addr'])