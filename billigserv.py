#!/usr/bin/python

import socket
import os

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host, port))
s.listen(5)

print("billiger HTTP-Server jetzt live auf ", host, ':', port)

while True:
    conn, clientaddr = s.accept()
    print('Verbindung erhalten von: ', clientaddr)

    # handle connection request here
    commandInfoList = str(conn.recv(4096), 'utf-8').split('\n',1)[0].split(' ')
    fileLocation = commandInfoList[1]
    httpCommand = commandInfoList[0]

    del commandInfoList

    if httpCommand == "GET":
        if fileLocation == "/":
            fileLocation = os.getcwd() + "/index.html"
        else:
            fileLocation = os.getcwd() + fileLocation
    
        inFile = open(fileLocation, 'rt')
        fileBytes = inFile.read().encode("utf-8")
        inFile.close()

        conn.send(fileBytes)

    # finally close connection
    conn.close()
