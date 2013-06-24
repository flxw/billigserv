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

def buildResponseHeader(status):
    responseDict = { 200 : "HTTP/1.1 200 OK",
                   400 : "HTTP/1.1 400 Bad Request",
                   404 : "HTTP/1.1 404 File not found" }

    header  =  responseDict[statusCode] + "\n"
    header  += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\n")
    header  += "Content-Type: text/html\n"
    header  += "Content-Encoding: UTF-8\n"
    header  += "Server: getsome\n"

    return header

def sendResponse(sinkSocket, statusCode, responseContent=""):
    """sinkSocket = Socket that data will be sent to
       statusCode = integer with HTTP response code
       responseContent = string that contains the response body"""

    responseHeader = buildResponseHeader(statusCode)
    
    sinkSocket.send(responseHeader.encode("utf-8"))
    sinkSocket.send(responseContent.encode("utf-8"))

    # finally close connection
    sinkSocket.close()

def handleRequestInThread(clsock):
    # handle connection request here
    commandInfoList = str(clsock.recv(4096), 'utf-8').split('\n',1)[0].split(' ')

    if len(commandInfoList) < 2:
        print("strange list received: ", commandInfoList)
        sendResponse(clsock, 400)
        return;

    fileLocation = commandInfoList[1]
    httpCommand = commandInfoList[0]

    del commandInfoList

    statusCode = None;
    body       = "";

    if httpCommand == "GET":
        fileLocation = buildLocationString(fileLocation)

        if fileLocation != None:
            inFile = open(fileLocation, 'rt')
            body = inFile.read()
            statusCode    = 200;
            inFile.close()
        else:
            statusCode = 404;
    else:
        statusCode = 400;

    sendResponse(clsock, statusCode, body)


if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    port = 8888
    s.bind((host, port))
    s.listen(5)

    print("Come and GET some at ", host, 'on port ', port, '!')

    while True:
        conn, clientaddr = s.accept()

        t = threading.Thread(target=handleRequestInThread, args=[conn])
        t.start()
        print('Handling request from ', clientaddr, ' in thread with ID \'', t.name, '\'')
