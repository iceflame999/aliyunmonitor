#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
import datetime
import smtplib
from email.mime.text import MIMEText


def send_msg(add, mail):


    # html表格头部
    htmla = """
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<body>
<p><strong>检测到RDS性能增加，请保持关注:</strong></p>
 <table style="width:80%;font-size:20px;" cellpadding="2" cellspacing="0" border="1" bordercolor="#000000">
<tr>
  <td rowspan="2"><strong>主机名</strong></td>
  <td colspan="4"><strong>cpu使用情况（%）</strong></td>
  <td colspan="4"><strong>内存使用情况（G）</strong></td>
  <td colspan="4"><strong>磁盘使用量（%）</strong></td>
  <td colspan="4"><strong>iops使用率</strong></td>
  <td colspan="4"><strong>连接数使用率</strong></td>
</tr>
<tr>
<td>8天前</td><td>2天前</td><td>1天前</td><td>cpu负载增加</td>
<td>8天前G</td><td>2天前</td><td>1天前</td><td>内存使用率增长（%）</td>
<td>8天前</td><td>2天前</td><td>1天前</td><td>磁盘使用率增加</td>
<td>8天前</td><td>2天前</td><td>1天前</td><td>iops使用率增长（%）</td>
<td>8天前</td><td>2天前</td><td>1天前</td><td>连接数使用率增长（%）</td>
</tr>
"""
    # html表格尾部
    htmlb = """
</table>
</body>
</html>
    """
    # html表格内容，通过mail动态添加
    k = len(mail)
    i = 0
    while i < k:
        if int(mail[i][5]) > 7:
            bgcolor1 = '#ff8080'  # 单元格背景色
        else:
            bgcolor1 = ''
        if int(mail[i][9]) > 7:
            bgcolor2 = '#ff8080'
        else:
            bgcolor2 = ''
        if int(mail[i][13]) > 7:
            bgcolor3 = '#ff8080'
        else:
            bgcolor3 = ''
        if int(mail[i][17]) > 10:
            bgcolor4 = '#ff8080'
        else:
            bgcolor4 = ''
        if int(mail[i][21]) > 10:
            bgcolor5 = '#ff8080'
        else:
            bgcolor5 = ''
        row = "<tr><td>" + str(mail[i][0]) + "</td><td>" + str(round(mail[i][2], 2)) + "</td><td>" + str(
            round(mail[i][3], 2)) + "</td><td>" + str(
            round(mail[i][4], 2)) + "</td><td bgcolor='" + bgcolor1 + "'>" + str(
            round(mail[i][5], 2)) + "</td><td>" + str(round(mail[i][6], 2)) + "</td><td>" + str(
            round(mail[i][7], 2)) + "</td><td>" + str(
            round(mail[i][8], 2)) + "</td><td bgcolor='" + bgcolor2 + "'>" + str(
            round(mail[i][9], 2)) + "</td><td>" + str(
            round(mail[i][10], 2)) + "</td><td>" + str(round(mail[i][11], 2)) + "</td><td>" + str(
            round(mail[i][12], 2)) + "</td><td bgcolor='" + bgcolor3 + "'>" + str(
            round(mail[i][13], 2)) + "</td><td>" + str(
            round(mail[i][14], 2)) + "</td><td>" + str(round(mail[i][15], 2)) + "</td><td>" + str(
            round(mail[i][16], 2)) + "</td><td bgcolor='" + bgcolor4 + "'>" + str(
            round(mail[i][17], 2)) + "</td><td>" + str(
            round(mail[i][18], 2)) + "</td><td>" + str(round(mail[i][19], 2)) + "</td><td>" + str(
            round(mail[i][20], 2)) + "</td><td bgcolor='" + bgcolor5 + "'>" + str(
            round(mail[i][21], 2)) + "</td></tr>"
        htmla = htmla + row
        i = i + 1
    html = htmla + htmlb
    msg_from = 'fuwuqifuzai@roobo.com'  # 发送方邮箱
    passwd = 'Ai123456'  # 填入发送方邮箱的授权码
    msg_to = add  # 收件人邮箱

    subject = "RDS性能监测预警7天"  # 主题
    msg = MIMEText(html, _subtype='html', _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print
        "发送成功", msg_to
        s.quit()
        return 1
    except:
        print
        "发现异常！！！！！！！！！！！！！"
        print
        msg_to
        return 0



def get_alarm(name, date):
    sql = "select * from rds_alarm where name = '" + name + "' and date = '" + str(date) + "';"
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    db.close()
    return cur1

def get_hosts():
    hosts = []
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    sql = "select `name` from rds_instanceid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hosts.append(cur1[0])
        cur1 = cursor.fetchone()
    return hosts

yesterday = datetime.date.today() + datetime.timedelta(days=-1)
mail = []
hosts = get_hosts()
for host in hosts:
    mail0 = get_alarm(host,yesterday)
    if mail0:
	mail.append(mail0)
if mail:
    print mail
    send_msg('op@roobo.com', mail)
