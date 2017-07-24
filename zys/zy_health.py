#!/usr/bin/python3


import mysql.connector as mdb


class zhouyi:

    def __init__(self,):
        self.trig_dict={
            1:"7",
            2:"3",
            3:"5",
            4:"1",
            5:"6",
            6:"2",
            7:"4",
            8:"0"
        }

    def trigram(self,day):
        tg_up=0
        tg_down=0
        change_yao = 0
        try:
            for c in day[0:6]:
                tg_up += int(c,10)
            for c in day[4:8]:
                tg_down += int(c,10)
            
            i=0
            end = len(day)
            for i in range(0,end):
                if not day[i]=="0":
                    change_yao += int(day[i])
                elif not i==4:
                    change_yao += 8
            tg_up %= 8
            if tg_up==0:
                tg_up=8
            tg_down %= 8
            if tg_down == 0:
                tg_down = 8
            change_yao %= 6
            if change_yao == 0:
                change_yao = 6
        except (ValueError,e):
            print (e)
            return (-1,-1,-1)
        except:
            print ("error:get trigram")
            return (-1,-1,-1)

        up = self.trig_dict[tg_up]
        down = self.trig_dict[tg_down]

        return (int(up,10), int(down,10), change_yao)


    def gener_trig(self,tg_tuple):
        try:
            tg_up = tg_tuple[0]
            tg_down = tg_tuple[1]
            tg_change = tg_tuple[2]
            self_trig = str(tg_up)+str(tg_down)

            tg_midup = ((3&tg_up)<<1)+((4&tg_down)>>2)
            tg_middown = ((1&tg_up)<<2)+(tg_down>>1)
            mid_trig = str(tg_midup) + str(tg_middown)

            tg_buf = (tg_up<<3)+tg_down
            tch = tg_change-1
            if (tg_buf>>tch)&1:
                tg_buf &= (63^(1<<tch))
            else:
                tg_buf |= 1<<tch

            tg_chup = tg_buf >> 3
            tg_chdown = tg_buf & 7
            chang_trig = str(tg_chup) + str(tg_chdown)
            
        except:
            print ("error: generation trigram")
            return ("--","--","--")
        return (self_trig, mid_trig, chang_trig)
        

    def trigram_tuple_str(self,tg_tuple):
        return str(tg_tuple[0]) + str(tg_tuple[1]) + str(tg_tuple[2])

    def common_handle(self,day):
        g = self.trigram(day)
        if g == (-1,-1,-1):
            return "--failed"
        gt = self.gener_trig(g)
        if gt == ("--","--","--"):
            return "--failed"
        tg = self.trigram_tuple_str(gt)
        return tg


class zy_health(zhouyi):
    def __init__(self,):
        self.health_db=""
        self.birthday_len = 8
        try:
            self.health_db = mdb.connect(host="localhost",user="root",passwd="101",database="zhouyi")
            self.cur = self.health_db.cursor()
            self.cur.execute("set names utf8")
        except(mdb.errors,e):
            print (e)
        except:
            print ("error:unknow at health module")

    def health_req_check(self,req):
        if len(req)==self.birthday_len and re.search("[0-9]{8}",req[1]) == None:
           return "unknow request"
        return req[1]

    def health_sql(self,trigram):
        try:
            cur = self.health_db.cursor()
            trigram_list=[]
            i=0
            while i < 6:
                inst_sql="select * from g where coding="+trigram[i:i+2]
                cur.execute(inst_sql)
                tg = cur.fetchone()
                trigram_list.append(tg[1])
                i += 2
        except:
            print ("error: python query mysql")
            return "--failed"

        return trigram_list

    def health_info(self,req):
        birthday = self.health_req_check(req)
        if birthday == "unknow request":
            return birthday
        trig = zhouyi().common_handle(birthday)
        if not trig == "--failed":
            return self.health_sql(trig)
        else:
            return trig


