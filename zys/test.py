#!/usr/bin/python2.7

#coding=utf-8
'''
import MySQLdb as mdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
url="http://192.168.1.106/?p="
alist=[]
list_sql='select ID,post_title,post_date from wp_posts where post_status="publish" and post_type="post"'
artdb = mdb.connect("localhost","root","101","wp_zhouyi")
cur = artdb.cursor()
cur.execute("set names utf8")
cur.execute(list_sql)
line = cur.fetchone()
while line:
    alist.append((line[1],line[2],url+str(line[0])))
    line = cur.fetchone()

for f in alist:
    print f[0],f[2]
'''

from zy_article import *

art = article()
art.get_list(10)
