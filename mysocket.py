'''
Created on 2019年3月21日

@author: zjf
'''
import websocket
import json
import time
import base64
import sys
import os
import psutil   
import socket

import threading
import sys
from time import ctime



class mySocket():

    def __init__(self,msgcallback):
        self.msgcallback = msgcallback
        self.clientList=[]
        self.sock = None
    
    def connect(self,host_ip, host_port):
        self.sock = socket.socket()
        self.sock.settimeout(20)
        try:
            self.sock.connect((host_ip, host_port))
            self.sock.settimeout(None)
            threading.Thread(target=self.doReceive, args=(self.sock,)).start()
        except socket.error as e:
            print("Socket Connect Error:%s" % e)
            exit(1)
        
    def startListen(self,port):
        tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# as s:
        tcpSerSock.bind(("0.0.0.0", port))
        tcpSerSock.listen(5)
        while True:
            conn, addr = tcpSerSock.accept()
            # print('Connected by', addr)
            threading.Thread(target=self.doReceive, args=(conn,)).start()

        tcpSerSock.close()
    
    def close(self):
        self.sock.close()

    def doReceive(self,conn):
        self.clientList.append(conn)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                if self.msgcallback is not None:
                    self.msgcallback(data.decode())
            except socket.error as e:
                # print('socket running error:', str(e))
                break
        self.clientList.remove(conn)
    
    def sendMsg(self,msg):
        for item in self.clientList:
            item.sendall(bytearray(msg.encode()))
        # if self.sock is not None:
        #     self.sock.sendall(bytearray(msg.encode()))

def callbk1(msg):
    print(msg)

def callbk2(msg):
    # print(msg)
    s.sendMsg(msg)

if __name__ == '__main__':
    choosetype ='server'
    if len(sys.argv) > 1 and sys.argv[1] =='client':
        choosetype = 'client'
    if len(sys.argv) > 1 and sys.argv[1] =='server':
        choosetype = 'server'

    if choosetype =="client":
        s = mySocket(callbk1)
        s.connect("127.0.0.1",82)
        while True:
            msg = input('SERVER >> ')
            if msg =="end":
                break
            s.sendMsg(msg)
        s.close()
        print(2)
    else:
        s = mySocket(callbk2)
        s.startListen(82)


