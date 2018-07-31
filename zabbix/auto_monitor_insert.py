#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
import datetime
import smtplib
from email.mime.text import MIMEText

#存放hostid
hostid = []

def timestamp_datetime(value):
    format = '%Y-%m-%d'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     #time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     time.strptime(dt, '%Y-%m-%d')
     s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
     return int(s)

#获取hostid
def gethostid():
    db = MySQLdb.connect()
    cursor = db.cursor()
    sql = "select hostid,host,status from hosts where hostid >10100 and status=0 order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    return hostid

def gethostname(hostid):
    db = MySQLdb.connect()
    cursor = db.cursor()
    sql = "select host from hosts where hostid =" +str(hostid) + ";"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    db.close()
    return cur1[0]


def gethostid_avg():
    db = MySQLdb.connect()
    cursor = db.cursor()
    sql = "select distinct hostid from avg_free where date ='"+ str(today_0) + "' order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    db.close()
    return hostid
  
#从avg数据表读取数据
def get_avg(hostid,date):
    sql = "SELECT cpu_idle,mem_free,disk_free,avg_tcp from avg_free where hostid = " + str(hostid) + " and date = '" + str(date) + "';"
    db = MySQLdb.connect()
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    if data :
        return data
    else :
	return (0,0,0,9999)

def gettotalmem(hostid):
    today = datetime.date.today()
    today_unix = datetime_timestamp(str(today))
    db = MySQLdb.connect()
    cursor = db.cursor()
    sql = "select itemid from items where hostid =" +str(hostid) + " and key_ ='vm.memory.size[total]';"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    itemid = cur1[0]
    sql = "select `value` from history_uint where itemid ="+ str(itemid)+" and clock >"+str(today_unix) +" ;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    db.close()
    return cur1[0]



def insert_alarm(date,mail):
    k = len(mail)
    i = 0
    db = MySQLdb.connect()
    cursor = db.cursor()
    while i<k:
	yesterday = get_avg(mail[i][4],date)
	today_7 = date + datetime.timedelta(days=-7)
	ago7 = get_avg(mail[i][4],today_7)
        today_1 = date + datetime.timedelta(days=-1)
        ago1 = get_avg(mail[i][4],today_1)
	total = gettotalmem(mail[i][4])
	sql = "INSERT into alarm VALUES('" + str(mail[i][0]) + "','" + str(date) + "',"+str(round((100-ago7[0]),1))+"," +str(round((100-yesterday[0]),1))+","+ str(round(mail[i][1],1)) + ","+str(round(ago7[1]/1073741824.00,2))+"," +str(round(yesterday[1]/1073741824.00,2))+"," + str(round(mail[i][2],2)) + ","+str(round((100-ago7[2]),1))+"," +str(round((100-yesterday[2]),1))+"," + str(round(mail[i][3],1)) +"," +str(round(total/1073741824.00,2))+"," + str(round((100-ago1[0]),1))+","+str(round(ago1[1]/1073741824.00,2))+","+str(round((100-ago1[2]),1))+","+ str(round(ago7[3],0))+","+str(round(ago1[3],0))+","+str(round(yesterday[3],0))+","+str(round(mail[i][5],1)) +");"
	cursor.execute(sql)
        db.commit()
	i = i+1
    db.close()



today = datetime.date.today()
today_0 = today + datetime.timedelta(days=-1)
today_1 = today + datetime.timedelta(days=-2)
today_2 = today + datetime.timedelta(days=-3)
today_3 = today + datetime.timedelta(days=-4)
today_4 = today + datetime.timedelta(days=-5)
today_5 = today + datetime.timedelta(days=-6)
today_6 = today + datetime.timedelta(days=-7)
today_7 = today + datetime.timedelta(days=-8)
week = (today_0,today_1,today_2,today_3,today_4,today_5,today_6,today_7)


mail = []   #邮件内容
hostid = gethostid_avg()
for host in hostid :
    
    data_week = []  #保存取出来的数据
    #将数据添加到data_week中
    i =0
    while i<8 :
        data_week.append(get_avg(host,week[i]))
        i = i +1 
    i = 1
    k = 0
    cpu_ch = 0.0
    mem_ch = 0.0
    disk_ch = 0.0
    tcp_ch = 0.0
    #计算七天累计变动值
    try:
        while i<8 :
            cpu_ch= cpu_ch + data_week[i][0] - data_week[k][0]
            mem_ch= mem_ch + data_week[i][1] - data_week[k][1]
            disk_ch= disk_ch + data_week[i][2] - data_week[k][2]
	    tcp_ch = tcp_ch + data_week[k][3] - data_week[i][3]
            i = i + 1
            k = k + 1
    except:
	cpu_ch = 0.0
	mem_ch = 0.0
	disk_ch = 0.0
	tcp_ch = 9999
	print host,"lack of data!"
    if data_week[k][1] :
	mem_ch_per = mem_ch / data_week[k][1] * 100
    else :
	mem_ch_per = 0
    if data_week[k][3]:
	tcp_ch_per = tcp_ch / data_week[k][3] * 100
    else:
	tcp_ch_per = 0
    #mem_ch_per = data_week[k][1] / (mem_ch + 1)
    #设定报警的波动值
    name = str(gethostname(host))
    try:
        if (cpu_ch > 8 and data_week[k][0] <70) or (mem_ch_per > 10 ) or (disk_ch > 8) or (tcp_ch_per > 10):
           mail.append((name,cpu_ch,mem_ch_per,disk_ch,host,tcp_ch_per))
	   print name,cpu_ch,mem_ch_per,disk_ch
        else:
            print host,"正 常"
            print name,cpu_ch,mem_ch_per,disk_ch
    except Exception ,e:
	print str(e.message)
	mail.append((host,"异 常"))
	print host,name,"异 常"

if mail:
    insert_alarm(today_0,mail)
    
else:
    print "all device is normal !"



