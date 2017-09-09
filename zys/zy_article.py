#!/usr/bin/python3


import mysql.connector as mdb
import sys
import time

class article:
    def __init__(self,):
        self.req_list = ["list",]
        self.artdb = ""
        self.cur = ""
        self.counts=10
        #self.url="http://192.168.1.106/?p="
        self.alist=[]
        self.a_text="{name:%s,date:%s,url:%s}"
        self.end_index=0
        self.list_sql='select post_title,post_date,guid from wp_posts where post_status="publish" and post_type="post"'
        try:
            self.artdb = mdb.connect(host="localhost",user="root",passwd="101",database="wp_zhouyi")
            self.cur = self.artdb.cursor()
            self.cur.execute("set names utf8")
            self.cur.execute(self.list_sql)
            line = self.cur.fetchone()
            list_buf=[]
            while line:
                list_buf.append((line[0],line[1],line[2]))
                line = self.cur.fetchone()
            self.alist = sorted(list_buf,key=lambda d: d[1],reverse=True)
            list_buf=[]
            self.end_index = len(self.alist)
        except TypeError as e:
            print (e)
        except mdb.Error as e:
            print (e)
        except:
            print ("error:unknow")


    def article_req_check(self,req_list):
        req_buf = req_list[1:len(req_list)]
        if req_buf[0] in self.req_list:
            return req_buf
        else:
            return "unknow request" 


#sorted(data,lambda d:d[1],reverse=True)

    def get_article_list(self,):
        try:
            self.cur = self.artdb.cursor()
            self.cur.execute(self.list_sql)
            line = self.cur.fetchone()
            list_buf=[]
            while line:
                list_buf.append((line[0],line[1],line[2]))
                line = self.cur.fetchone()
            self.alist = sorted(list_buf,key=lambda d: d[1],reverse=True)
            list_buf=[]
            self.end_index = len(self.alist)
        except mdb.Error as e:
            print(e)
        

    def get_list(self,number=0):
        al=[]
        if number>=self.end_index:
            return ["no articles",]
        for a in self.alist[number:self.counts+number]:
            al.append(self.a_text%a)
        return al

    def search_list(self,keywords):
        pass

    def get_update(self,):
        self.alist=[]
        self.end_index=0
        self.get_article_list()


    def articles(self,req_list):
        r = self.article_req_check(req_list)
        if r=="unknow request":
            return r
        elif r[0] == "list":
            return self.get_list(int(r[1],10))
        
