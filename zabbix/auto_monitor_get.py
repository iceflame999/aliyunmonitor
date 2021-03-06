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
    sql = "select hostid,host,status from hosts where hostid > 10100 and status=0 order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    return hostid

def gethostid_avg():
    db = MySQLdb.connect()
    cursor = db.cursor()
    sql = "select distinct hostid from avg_free order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    return hostid


    

def getavg(date,host):#####获取指定日期的峰值
    #获取当前日期，找到unixtime对应的最小值和最大值
    #today = datetime.date.today()
    today = date
    yesterday = today + datetime.timedelta(days=-1)
    #print today
    today_unix = datetime_timestamp(str(today))
    yesterday_unix = datetime_timestamp(str(yesterday))

    # 打开数据库连接
    db = MySQLdb.connect()

    # 获取操作游标 
    cursor = db.cursor()

    #根据hostid获取itemid
    sql = "select itemid FROM items WHERE hostid ='" + str(host) + "' and (key_='system.cpu.util[,idle]' or key_='vm.memory.size[available]' or key_='vfs.fs.size[/,pfree]' or key_='tcp_conn[COUNT]') ORDER BY `name`;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    mem_itemid = cur1[0]
    cur1 = cursor.fetchone()
    cpu_itemid = cur1[0]
    cur1 = cursor.fetchone()
    disk_itemid = cur1[0]
    cur1 = cursor.fetchone()
    if cur1:
        tcp_itemid = cur1[0]
    else:
	tcp_itemid = 0

    # 执行查询cpu_idle,SQL语句
    sql = "select clock,`value` FROM history WHERE `itemid`=" + str(cpu_itemid) + " and clock > "+ str(yesterday_unix) +" and clock <"+ str(today_unix) + ' order by `value`;'
    cursor.execute(sql)
    data = []
    #print "cpu:",sql
    avg_idle = 0 
    # 使用 fetchone() 方法获取一条数据
    for i in range(0,100):
	cur1 = cursor.fetchone()
	if cur1:
            data.append(cur1)
	    avg_idle =avg_idle + data[i][1]
	else:
	    data.append((0,0))
	    avg_idle = avg_idle + data[i][1]
    #data = cursor.fetchone()
    #print data
    avg_idle = avg_idle / 100

    #print avg_idle

    # 执行查询memory_freeSQL语句
    sql = "select clock,`value` FROM history_uint WHERE `itemid`=" + str(mem_itemid) + " and clock > "+ str(yesterday_unix) +" and clock <"+ str(today_unix) + ' order by `value`;'
    #print sql
    cursor.execute(sql)
    data = []
    #print "mem:",sql
    avg_mem = 0 
    # 使用 fetchone() 方法获取一条数据
    for i in range(0,100):
	cur1 = cursor.fetchone()
        if cur1:
            data.append(cur1)
            avg_mem =avg_mem + data[i][1]
        else:
            data.append((0,0))
            avg_mem = avg_mem + data[i][1]
    #data = cursor.fetchone()
    #print data
    avg_mem = avg_mem / 100
# 执行查询disk_freeSQL语句
    sql = "select clock,`value` FROM history WHERE `itemid`=" + str(disk_itemid) + " and clock > "+ str(yesterday_unix) +" and clock <"+ str(today_unix) + ' order by `value`;'
    #print sql
    cursor.execute(sql)
    data = []
    #print "disk:",sql
    avg_disk = 0 
    # 使用 fetchone() 方法获取一条数据
    for i in range(0,100):
	cur1 = cursor.fetchone()
        if cur1:
            data.append(cur1)
            avg_disk =avg_disk + data[i][1]
        else:
            data.append((0,0))
            avg_disk = avg_disk + data[i][1]
    #data = cursor.fetchone()
    #print data
    avg_disk = avg_disk / 100

    #print avg_disk

# get tcp connect 
    sql = "select clock,`value` FROM history_uint WHERE `itemid` =" + str(tcp_itemid)+"  and clock > "+ str(yesterday_unix) +" and clock < "+ str(today_unix) +" order by `value` desc;"
    #print sql
    cursor.execute(sql)
    data = []
    #print "disk:",sql
    avg_tcp = 0
    # 使用 fetchone() 方法获取一条数据
    for i in range(0,10):
        cur1 = cursor.fetchone()
        if cur1:
            data.append(cur1)
            avg_tcp =avg_tcp + data[i][1]
        else:
            data.append((0,0))
            avg_tcp = avg_tcp + data[i][1]
    avg_tcp = avg_tcp / 10


    # 关闭数据库连接
    db.close()

    avg=[avg_idle,avg_mem,avg_disk,avg_tcp]

    return avg
#向avg数据表添加数据
def insert_avg(hostid,date,avg_cpu,avg_mem,avg_disk,avg_tcp) :
    ##
    yesterday = date + datetime.timedelta(days=-1)
    sql = "INSERT into avg_free VALUES(" + str(hostid) + ",'" + str(yesterday) + "'," + str(avg_cpu) + "," + str(avg_mem) + "," + str(avg_disk)+ ","+ str(avg_tcp)+ ");"

    db = MySQLdb.connect()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    print hostid,yesterday,avg_cpu,avg_mem,avg_disk,avg_tcp

#从avg数据表读取数据
def get_avg(hostid,date):
    sql = "SELECT cpu_idle,mem_free,disk_free from avg_free where hostid = " + str(hostid) + " and date = '" + str(date) + "';"
    db = MySQLdb.connect()
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data
today = datetime.date.today()



hostid = gethostid()
for host in hostid :
       
    a = getavg(today,host)   #获取设备数据
    insert_avg(host,today,a[0],a[1],a[2],a[3])    #插入记录表






