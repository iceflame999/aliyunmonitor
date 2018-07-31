#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import datetime


# 读取所有在运行RDS服务器ID，该表需要手工维护
def getinstanceid():
    instanceID = []
    db = MySQLdb.connect()
    cursor = db.cursor()
    sql = "select instanceid,`name` from rds_instanceid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        instanceID.append((cur1[0], cur1[1]))
        cur1 = cursor.fetchone()
    return instanceID


# 读取设备的数据
def get_value(date, instanceid):
    sql = "SELECT avg_cpu,avg_mem,avg_disk,avg_iops,avg_conn from rds_avg where instanceid = '" + str(
        instanceid) + "' and date = '" + str(date) + "';"
    db = MySQLdb.connect()
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    if data:
        return data
    else:
        return (99, 99, 99, 99, 99)


#

# 将预警设备及相应值插入rds_alarm数据库
def insert_alarm(date, alarm):
    k = len(alarm)
    i = 0
    db = MySQLdb.connect()
    cursor = db.cursor()
    while i < k:
        sql = "INSERT into rds_alarm VALUES('" + str(alarm[i][1]) + "','" + str(date) + "'," + str(
            round(alarm[i][2][1][0], 2)) + "," + str(round(alarm[i][2][2][0], 2)) + "," + str(
            round(alarm[i][2][0][0], 2)) + "," + str(round(alarm[i][2][0][0] - alarm[i][2][1][0], 2)) + "," + str(
            round(alarm[i][2][1][1], 2)) + "," + str(round(alarm[i][2][2][1], 2)) + "," + str(
            round(alarm[i][2][0][1], 2)) + "," + str(round(alarm[i][2][0][1] - alarm[i][2][1][1], 2)) + "," + str(
            round(alarm[i][2][1][2], 2)) + "," + str(round(alarm[i][2][2][2], 2)) + "," + str(
            round(alarm[i][2][0][2], 2)) + "," + str(round(alarm[i][2][0][2] - alarm[i][2][1][2], 2)) + "," + str(
            round(alarm[i][2][1][3], 2)) + "," + str(round(alarm[i][2][2][3], 2)) + "," + str(
            round(alarm[i][2][0][3], 2)) + "," + str(round(alarm[i][2][0][3] - alarm[i][2][1][3], 2)) + "," + str(
            round(alarm[i][2][1][4], 2)) + "," + str(round(alarm[i][2][2][4], 2)) + "," + str(
            round(alarm[i][2][0][4], 2)) + "," + str(round(alarm[i][2][0][4] - alarm[i][2][1][4], 2)) + ");"
        print sql
	cursor.execute(sql)
        db.commit()
        i = i + 1
    db.close()


# 设定日期，昨天，八天前，二天前
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
day_8 = datetime.date.today() + datetime.timedelta(days=-8)
day_2 = datetime.date.today() + datetime.timedelta(days=-2)

alarm = []  # 预警信息
instanceID = getinstanceid()
for instance in instanceID:

    data_week = []  # 保存取出来的数据
    # 将数据添加到data_week中
    data_week.append(get_value(yesterday, instance[0]))
    data_week.append(get_value(day_8, instance[0]))
    data_week.append(get_value(day_2, instance[0]))

    # 计算七天变动值
    cpu_ch = data_week[0][0] - data_week[1][0]
    mem_ch = data_week[0][1] - data_week[1][1]
    disk_ch = data_week[0][2] - data_week[1][2]
    iops_ch = data_week[0][3] - data_week[1][3]
    conn_ch = data_week[0][4] - data_week[1][4]

    # 设定报警的波动值
    if (cpu_ch > 7) or (mem_ch > 7) or (disk_ch > 7) or (iops_ch > 10) or (conn_ch > 10) or data_week[0][0] > 70 or \
            data_week[0][1] > 80 or data_week[0][2] > 90 or data_week[0][3] > 70 or data_week[0][4] > 70:
        alarm.append((instance[0], instance[1], data_week))
        print instance[0], instance[1], cpu_ch, mem_ch, disk_ch, iops_ch, conn_ch
    else:
        print instance[1], "正 常"
if alarm:
    insert_alarm(yesterday, alarm)
