#!/usr/bin/python

import socket

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host, port))
s.listen(5)

print("billig HTTP-Server jetzt live auf ", host, ':' port)

while True:
    conn, clientaddr = s.accept()
    print('Got connection from ', clientaddr)
    conn.close()
