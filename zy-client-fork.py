

import os
import sys
import socket
import time


def setup():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(("192.168.1.106",1990))
    return sock

request = "health:19900810"

req_year = 1960
req_year_end = 2015

req_mon = 1
req_mon_end = 12

req_day = 1
req_day_end = 29

answer = ""


for y in range(req_year,req_year_end):
    for m in range(req_mon,req_mon_end+1):
        for d in range(req_day,req_day_end+1):
            request = "health:"+str(y)
            m_buf = str(m)
            d_buf = str(d)
            if len(m_buf)==1:
                m_buf = "0"+m_buf
            if len(d_buf) == 1:
                d_buf = "0"+d_buf
            request += m_buf + d_buf
            print request[7:15]
            sock = setup()
            sock.sendall(request)
            while True:
                buf = sock.recv(1024)
                if len(buf) == 0:
                    break
                answer += buf
            a_buf = answer.rstrip('<end>')
            a_end = a_buf.split('--ok--')
            for l in a_end:
                print l
            answer = ""
            sock.close()



