#!/usr/bin/env python
# coding=utf-8
# 每天从阿里云获取实例的性能参数，保存到本地数据库中。
import rooboaliyun
import datetime
import MySQLdb

yesterday = datetime.date.today() + datetime.timedelta(days=-1)
instanceID = []

# 读取所有在运行RDS服务器ID，该表需要手工维护
def getinstanceid():
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    sql = "select instanceid,`name` from redis_instanceid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        instanceID.append((cur1[0],cur1[1]))
        cur1 = cursor.fetchone()
    return instanceID

def getavg(date, instanceid):#####获取指定日期的峰值
    a = rooboaliyun.rooboaliyun()
    cpu = a.get_cpu(instanceid, date)
    mem = a.get_mem(instanceid, date)
    intranetin = a.get_in(instanceid, date)
    intranetout = a.get_out(instanceid, date)
    return [cpu, mem, intranetin, intranetout]

# 向avg数据表添加数据
def insert_avg(instanceid, name, date, avg_cpu, avg_mem, avg_in, avg_out):
    ##
    sql = "INSERT into redis_avg VALUES('" + str(instanceid) + "','" + str(name) + "','" + str(date) + "'," + str(avg_cpu) + "," + str(avg_mem) + "," + str(avg_in) + "," + str(avg_out) + ");"
    print sql
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    print instanceid, date, avg_cpu, avg_mem, avg_in, avg_out



instanceID = getinstanceid()
for instance in instanceID:
    a = getavg(yesterday, instance[0])  # 获取设备数据
    insert_avg(instance[0], instance[1], yesterday, a[0], a[1], a[2], a[3])  # 插入记录表


