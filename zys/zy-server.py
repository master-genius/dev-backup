#!/usr/bin/python3

import os
import re
import sys
import threading
import socket
import sys
import select
from zy_health import *

class req_handle:
    def __init__(self,):
        self.req_max_len = 64 
        self.req_list=["health","article","info",]
        self.req_dict={
            "health":zy_health().health_info,
        }

    def type_analysis(self,usr_req):
        
        req = str(usr_req,encoding="utf-8")[0:self.req_max_len]
        req = req.strip(":")
        if not ":" in req:
            return "unknow request"
        req_protocol = req.split(":")
        if not req_protocol[0] in self.req_list:
            return "unknow request"
        else:
            return req_protocol

    def commander(self,req):
        req_list = self.type_analysis(req)
        if req_list== "unknow request":
            return req_list
        else:
            return self.req_dict[req_list[0]](req_list)


class epoll_server:
    def __init__(self,):
        self.ip_address = "192.168.1.107"
        self.port = 1990
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.ip_address,1990))
        self.sock.listen(1024)
        self.sock.setblocking(0)
        self.epoll = select.epoll()
        self.epoll.register(self.sock.fileno(),select.EPOLLIN)
        self.req_handle = req_handle()

    def get_answer(self,request):
        return self.req_handle.commander(request)
         
    def send_answer(self,client_sock,answer):
        try:
            if type(answer) == type(""):
                client_sock.sendall(bytes(answer,encoding="utf-8"))
            elif type(answer) == type([]):
                for line in answer:
                    client_sock.sendall(bytes(line,encoding='utf-8'))
                    client_sock.sendall(bytes("--ok--",encoding="utf-8"))
            client_sock.sendall(bytes("<end>",encoding="utf-8"))
            client_sock.close()
        except socket.error as e:
            print (e)
        except:
            print ("error:send data")

    
    def server_run(self,):
        requests={}; connections={}; responses={}
        try:
            while True:
                events = self.epoll.poll(1)
                for fd,event in events:
                    if fd == self.sock.fileno():
                        client_sock, sockname = self.sock.accept()
                        print ("connected by",sockname)
                        client_sock.setblocking(0)
                        self.epoll.register(client_sock.fileno(),select.EPOLLIN)
                        connections[client_sock.fileno()] = client_sock

                    elif event & select.EPOLLIN:
                        requests[fd] = connections[fd].recv(128)
                        print ("get request",str(requests[fd],encoding='utf-8'))
                        self.epoll.modify(fd,select.EPOLLOUT)
                        responses[fd] = self.get_answer(requests[fd])

                    elif event & select.EPOLLOUT:
                        sock_buf = connections[fd]
                        self.send_answer(sock_buf,responses[fd])
                        
                    elif event & select.EPOLLHUP:
                        self.unregister(fd)
                        del connections[fd]

        except(KeyboardInterrupt):
            print ("\nBye ^_^")
            exit(0)
        finally:
            self.epoll.unregister(self.sock.fileno())
            self.epoll.close()
            self.sock.close()


epoll_server().server_run()

