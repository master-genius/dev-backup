#!/usr/bin/python2.7
#encdoingutf-8

import os
import socket
import sys

def setup():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.1.106",1990))
    return sock

#sock = setup()

inst_history=[]
req_buf = ''
answer = ""

while True:
    try:
        request = raw_input()
    except IOError,e:
        print e
        continue
    if request == "-q":
        break
    elif request == "-rc":
        sock.close()
        sock = setup()
        continue
    sock = setup()
    if not request == "-r":
        req_buf = request
    if request == "-r":
        request = req_buf
    try:
        sock.sendall(request)
        while True:
            buf = sock.recv(1024)
            if len(buf)==0:
                break
            answer += buf
    except:
        print "error:send request"

    answer_buf = answer.strip('<end>')
    answer_end = answer_buf.split('--ok--')
    for l in answer_end:
        print l

    sock.close()
    answer = ""

#sock.close()
