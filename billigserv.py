#!/usr/bin/python

import socket
import os
import time
import threading

def buildLocationString(reqPath):
    if reqPath == "/":
        reqPath = os.getcwd() + "/index.html"
    else:
        reqPath = os.getcwd() + reqPath

    if os.path.exists(reqPath):
        return reqPath
    else:
        return None

def handleRequestInThread(clsock):
        # handle connection request here
        commandInfoList = str(clsock.recv(4096), 'utf-8').split('\n',1)[0].split(' ')

        if len(commandInfoList) >= 2:
            fileLocation = commandInfoList[1]
            httpCommand = commandInfoList[0]

            del commandInfoList

            headerBytes  = ""
            answerBytes  = ""
            if httpCommand == "GET":
                fileLocation = buildLocationString(fileLocation)

                if fileLocation != None:
                    inFile = open(fileLocation, 'rt')
                    answerBytes = inFile.read().encode("utf-8")
                    inFile.close()
                    headerBytes = "HTTP/1.1 200 OK"
                else:
                    headerBytes = "HTTP/1.1 404 File Not Found"
            else:
                headerBytes = "HTTP/1.1 400 Bad Request"
        else:
            headerBytes = "HTTP/1.1 400 Bad Request"


        headerBytes += time.strftime('\nDate: %a, %d %b %Y %H:%M:%S GMT')
        headerBytes += "\nContent-Type: text/html"
        headerBytes += "\nX-Info: Billiger gehts nicht!\n"
        clsock.send(headerBytes.encode("utf-8"))
        clsock.send(answerBytes)

        # finally close connection
        clsock.close()

if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    port = 8080
    s.bind((host, port))
    s.listen(5)

    print("billiger HTTP-Server jetzt live auf ", host, ':', port)

    while True:
        conn, clientaddr = s.accept()

        t = threading.Thread(target=handleRequestInThread, args=[conn])
        t.start()
        print('Abarbeitung von Request ', clientaddr, ' in Thread ', t.name)
