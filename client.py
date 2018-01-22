# coding=utf-8
from socket import *

HOST = '127.0.0.1'
PORT = 8888
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


while True:
    data = input('> ')
    if not data:
        break
    print('sending data:',data,len(data.encode('utf-8')))
    tcpCliSock.send(data.encode('utf-8'))
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        break

    print(data.decode('utf-8'))

tcpCliSock.close()