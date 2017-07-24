#!/usr/bin/python3

import mysql.connector as mdb
import sys
import os
import time


class zy_info:
    def __init__(self,):
        self.news_path = "./news/"
        self.activity_path = "./activity/"
        self.req_list = ["news","activity"]

    def info_req_check(self,reqlist):
        if len(reqlist)==2 and reqlist[1] in self.req_list:
            return reqlist
        else:
            return "unknow request"

    
    def get_news(self,):
        try:
            news_files = os.listdir(self.news_path)
            if len(news_files)==0:
                return "There is no news"
            news_list = sorted(news_files,reverse=True)
        except (OSError,e):
            print (e)
            return "--failed"
        try:
            nwl=[]
            content=""
            for n in news_list[0:3]:
                fd = open(self.news_path+n,"r")
                dn = fd.readlines()
                for l in dn:
                    content += l
                nwl.append(content)
                content=""
                dn=""
                fd.close()
            return nwl
        except (IOError,e):
            print (e)
            return "--failed"
        finally:
            if not fd.closed:
                fd.close()


    def get_activity(self,):
        try:
            act = os.listdir(self.activity_path)
            act_files=[]
            for f in act:
                act_files.append(self.activity_path+f)
            if len(act_files)==0:
                return "There is no activity"
        except (OSError,e):
            print (e)
            return "--failed"
        try:
            act_list=[]
            content = ""
            for f in act_files:
                fd = open(f,"r")
                data = fd.readlines()
                for d in data:
                    content += d
                act_list.append(content)

                fd.close()
            return act_list
        except (IOError,e):
            print (e)
            return "--failed"
        except:
            return "--failed"
        finally:
            if not fd.closed:
                fd.close()

    def get_info(self,reqlist):
        r = self.info_req_check(reqlist)
        if r == "unknow request":
            return r
        if reqlist[1] == "news":
            return self.get_news()
        elif reqlist[1] == "activity":
            return self.get_activity()


