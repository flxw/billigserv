#!/usr/bin/python

import socket
import os

def buildLocationString(reqPath):
    if reqPath == "/":
        reqPath = os.getcwd() + "/index.html"
    else:
        reqPath = os.getcwd() + reqPath

    if os.path.exists(reqPath):
        return reqPath
    else:
        return None

if __name__ == '__main__':
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

        answerBytes  = None
        if httpCommand == "GET":
            fileLocation = buildLocationString(fileLocation)

            if fileLocation != None:
                inFile = open(fileLocation, 'rt')
                answerBytes = inFile.read().encode("utf-8")
                inFile.close()
            else:
                answerBytes = "Status: HTTP/1.1 404 File Not Found".encode("utf-8")
        else:
            answerBytes = "Status: HTTP/1.1 400 Bad Request".encode("utf-8")

        conn.send(answerBytes)

        # finally close connection
        conn.close()
