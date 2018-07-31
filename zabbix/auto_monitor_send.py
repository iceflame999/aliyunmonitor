#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
import datetime
import smtplib
from email.mime.text import MIMEText


today = datetime.date.today()
today_0 = today + datetime.timedelta(days=-1)
today_7 = today + datetime.timedelta(days=-7)


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
    #db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix")
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix" )
    cursor = db.cursor()
    sql = "select hostid,host,status from hosts where hostid >10100 and status=0 order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    return hostid

def gethostname(hostid):
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix" )
    cursor = db.cursor()
    sql = "select host from hosts where hostid =" +str(hostid) + ";"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    return cur1[0]


def gethostid_avg():
    #db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix")
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor" )
    cursor = db.cursor()
    sql = "select distinct hostid from avg_free order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    return hostid
  
#从avg数据表读取数据
def get_avg(hostid,date):
    sql = "SELECT cpu_idle,mem_free,disk_free from avg_free where hostid = " + str(hostid) + " and date = '" + str(date) + "';"
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data

def send_msg(add,mail) :
        #html表格头部
    htmla ="""
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<body>
<p><strong>检测到主机性能存在风险，请及时确认:</strong></p>
 <table style="width:80%;font-size:20px;" cellpadding="2" cellspacing="0" border="1" bordercolor="#000000">
<tr>
  <td rowspan="2"><strong>主机名</strong></td>
  <td colspan="4"><strong>cpu使用情况（%）</strong></td>
  <td colspan="5"><strong>内存使用情况（G）</strong></td>
  <td colspan="4"><strong>磁盘使用量（%）</strong></td>
  <td colspan="4"><strong>TCP连接情况</strong></td>
</tr>
<tr>
<td>8天前</td><td>2天前</td><td>1天前</td><td>cpu负载增加</td>
<td>8天前G</td><td>2天前</td><td>1天前</td><td>内存增长率（%）</td><td>总内存</td>
<td>8天前</td><td>2天前</td><td>1天前</td><td>磁盘使用率增加</td>
<td>8天前</td><td>2天前</td><td>1天前</td><td>TCP连接增长率（%）</td>
</tr>
"""
    #html表格尾部
    htmlb="""
</table>
</body>
</html>
    """
    #html表格内容，通过mail动态添加
    k = len(mail)
    i = 0
    while i<k:
	if int(mail[i][4])>7:
	    bgcolor1 ='#ff8080'  # 单元格背景色
	else:
	    bgcolor1 =''
	if int(mail[i][7])>9:
	    bgcolor2 ='#ff8080'
        else:
            bgcolor2 = ''
	if int(mail[i][10])>7:
	    bgcolor3 ='#ff8080'
	else:
	    bgcolor3 = ''
	if int(mail[i][18])>7:
	    bgcolor4 = '#ff8080'
        else:
            bgcolor4 =''
        row = "<tr><td>"+str(mail[i][0])+"</td><td>"+str(round(mail[i][2],1))+"</td><td>"+str(round(mail[i][12],1))+"</td><td>"+str(round(mail[i][3],1))+"</td><td bgcolor='"+bgcolor1+"'>"+str(round(mail[i][4],1))+"</td><td>"+str(round((mail[i][11]-mail[i][5]),2))+"</td><td>"+str(round((mail[i][11]-mail[i][13]),2))+"</td><td>"+str(round((mail[i][11]-mail[i][6]),2))+"</td><td bgcolor='"+bgcolor2+"'>"+str(round((mail[i][5]-mail[i][6])/(mail[i][11]-mail[i][6])*100,2))+"</td><td>"+str(round(mail[i][11],2))+"</td><td>"+str(round(mail[i][8],1))+"</td><td>"+str(round(mail[i][14],1))+"</td><td>"+str(round(mail[i][9],1))+"</td><td bgcolor='"+bgcolor3+"'>"+str(round(mail[i][10],1))+"</td><td>"+str(round(mail[i][15],0))+"</td><td>"+str(round(mail[i][16],0))+"</td><td>"+str(round(mail[i][17],0))+"</td><td bgcolor='"+bgcolor4+"'>"+str(round(mail[i][18],1))+"</td></tr>"
	htmla = htmla + row
        i = i+1
    html = htmla + htmlb
    msg_from = 'fuwuqifuzai@roobo.com'                                  #发送方邮箱
    passwd = 'Ai123456'                                   #填入发送方邮箱的授权码
    msg_to = add                                  #收件人邮箱
                            
    subject = "服务器负载增加预警7天"                                     #主题     
    msg = MIMEText(html,_subtype='html',_charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.exmail.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print "发送成功",msg_to
	s.quit()
	return 1
    except:
	print "发现异常！！！！！！！！！！！！！"
	print msg_to
        return 0




#取所有人名，
def getname():
    sql = "select distinct username from host;"
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    names = []
    cur1 = cursor.fetchone()
    while cur1:
	names.append(cur1[0])
	cur1 = cursor.fetchone()
    db.close()
    return names;

#取每个人所负责的机器名
def get_hosts(name):
    sql = "select hostname from host where username = '"+ name +"';"
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    host = []
    while cur1:
	host.append(cur1[0])
	cur1 = cursor.fetchone()
    db.close()
    return host

def get_alarm(name,date):
    sql = "select * from alarm where hostname = '"+ name + "' and date = '"+ str(date) +"';"
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    db.close()
    return cur1

names = getname()
for name in names :
    mail = []
    hosts = get_hosts(name)
    for host in hosts:
        mail0 = get_alarm(host,today_0)
        if mail0:
            mail.append(mail0)
    if mail:
        mailname = name + "@roobo.com"
        send_msg(mailname,mail)




