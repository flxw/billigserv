#!/usr/bin/python

import sys
import socket
import os
import time
import threading

def buildLocationStringAndStatus(reqPath):
    if reqPath == "/":
        reqPath = os.getcwd() + "/index.html"
    else:
        reqPath = os.getcwd() + reqPath

    if os.path.isfile(reqPath):
        return (reqPath, 200)
    else:
        return (os.getcwd() + "/404.html", 404)

def buildResponseHeader(status):
    responseDict = { 200 : "HTTP/1.1 200 OK",
                     400 : "HTTP/1.1 400 Bad Request",
                     404 : "HTTP/1.1 404 Not Found" }

    header  =  responseDict[status] + "\n"
    header  += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\n")
    header  += "Content-Type: text/html\n"
    header  += "Content-Encoding: UTF-8\n"
    header  += "Server: getsome\n\n"

    return header

def sendResponse(sinkSocket, statusCode, responseContent=""):
    """sinkSocket = Socket that data will be sent to
       statusCode = integer with HTTP response code
       responseContent = string that contains the response body"""

    response = buildResponseHeader(statusCode) + responseContent

    totalsent = 0
    while totalsent < len(response):
        totalsent += sinkSocket.send(response[totalsent:].encode('utf-8'))

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
        fileLocation, statusCode = buildLocationStringAndStatus(fileLocation)

        inFile     = open(fileLocation, 'rt')
        body       = inFile.read()
        inFile.close()
    else:
        statusCode = 400;

    sendResponse(clsock, statusCode, body)

if __name__ == '__main__':
    try:
        # "parse" commandline arguments
        port = int(sys.argv[1])

        s       = socket.socket()
        host    = socket.gethostname()
        threads = []

        s.bind((host, port))
        s.listen(5)

        print("Come and GET some at ", host, 'on port ', port, '!')

        while True:
            conn, clientaddr = s.accept()

            t = threading.Thread(target=handleRequestInThread, args=[conn])
            t.start()
            threads.append(t)

            print('Handling request from ', clientaddr, ' in thread with ID \'', t.name, '\'')
    
    except IndexError:
        print("Please pass the port getsome is supposed to serve on!")
        sys.exit(-1)

    except ValueError:
        print("Please pass getsome's port as the ONLY argument! No more and no less!")
        sys.exit(-2)

    except KeyboardInterrupt:
        print("Waiting for all clients to be served...")

        for t in threads:
            t.join

        print("...serving done! Have a nice day!")
        sys.exit(0)
