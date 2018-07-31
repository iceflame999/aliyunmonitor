#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
import datetime
import smtplib
from email.mime.text import MIMEText

# 存放hostid
hostid = []


def timestamp_datetime(value):
    format = '%Y-%m-%d'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    # 经过localtime转换后变成
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
     # dt为字符串
     # 中间过程，一般都需要将字符串转化为时间数组
     # time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     time.strptime(dt, '%Y-%m-%d')
     s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
     return int(s)


# 获取hostid
def gethostid():
    # db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix")
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
    db.close()
    return cur1[0]


def gethostid_avg():
    # db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix")
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor" )
    cursor = db.cursor()
    sql = "select distinct hostid from avg_free where date ='"+ str(today_0) + "' order by hostid;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        hostid.append(cur1[0])
        cur1 = cursor.fetchone()
    db.close()
    return hostid
  
# 从avg数据表读取数据
def get_avg(hostid,date):
    sql = "SELECT cpu_idle,mem_free,disk_free from avg_free where hostid = " + str(hostid) + " and date = '" + str(date) + "';"
    db = MySQLdb.connect("10.44.13.30", "zabbix", "zabbix", "monitor")
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    if data:
        return data
    else:
	return (0,0,0)

def gettotalmem(hostid):
    today = datetime.date.today()
    today_unix = datetime_timestamp(str(today))
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix")
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
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor")
    cursor = db.cursor()
    while i<k:
	yesterday = get_avg(mail[i][4],date)
	today_7 = date + datetime.timedelta(days=-7)
	ago7 = get_avg(mail[i][4],today_7)
	total = gettotalmem(mail[i][4])
	sql = "INSERT into alarm VALUES('" + str(mail[i][0]) + "','" + str(date) + "',"+str(round((100-ago7[0]),1))+"," +str(round((100-yesterday[0]),1))+","+ str(round(mail[i][1],1)) + ","+str(round(ago7[1]/1073741824.00,2))+"," +str(round(yesterday[1]/1073741824.00,2))+"," + str(round(mail[i][2],2)) + ","+str(round((100-ago7[2]),1))+"," +str(round((100-yesterday[2]),1))+"," + str(round(mail[i][3],1)) +"," +str(round(total/1073741824.00,2))+ ");"
        print sql
	cursor.execute(sql)
        db.commit()
	i = i+1
    db.close()


def send_msg(add, mail):

    # html表格头部
    htmla = """
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<body>
<p><strong>检测到主机性能存在风险，请及时确认:</strong></p>
 <table style="width:80%;font-size:20px;" cellpadding="2" cellspacing="0" border="1" bordercolor="#000000">
<tr>
  <td rowspan="2"><strong>主机名</strong></td>
  <td colspan="3"><strong>cpu使用情况（%）</strong></td>
  <td colspan="4"><strong>内存使用情况（G）</strong></td>
  <td colspan="3"><strong>磁盘使用量（%）</strong></td>
</tr>
<tr>
<td>30天前</td><td>1天前</td><td>cpu负载增加</td>
<td>30天前G</td><td>1天前</td><td>内存增长率（%）</td><td>总内存</td>
<td>30天前</td><td>1天前</td><td>磁盘使用率增加</td>
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
    i=0

    while i < k:
        if int(mail[i][3]) > 7:
            bgcolor1 = '#ff8080'
        else:
            bgcolor1 = ''
        if int(mail[i][6]) > 9:
            bgcolor2 = '#ff8080'
        else:
            bgcolor2 = ''
        if int(mail[i][10]) > 7:
            bgcolor3 = '#ff8080'
        else:
            bgcolor3 = ''
        row = "<tr><td>" + str(mail[i][0]) + "</td><td>" + str(mail[i][1]) + "</td><td>" + str(mail[i][2]) + "</td><td bgcolor='" + bgcolor1 + "'>" + str(mail[i][3]) + "</td><td>" + str(mail[i][4]) + "</td><td>" + str(mail[i][5]) + "</td><td bgcolor='" + bgcolor2 + "'>" + str(mail[i][6]) + "</td><td>" + str(mail[i][7]) + "</td><td>" + str(mail[i][8]) + "</td><td>" + str(mail[i][9]) + "</td><td bgcolor='" + bgcolor3 + "'>" + str(mail[i][10]) + "</td></tr>"
        htmla = htmla + row
        i = i + 1
    html = htmla + htmlb
    msg_from = 'fuwuqifuzai@roobo.com'  # 发送方邮箱
    passwd = 'Ai123456'  # 填入发送方邮箱的授权码
    msg_to = add  # 收件人邮箱

    subject = "服务器负载增加预警1月"  # 主题
    msg = MIMEText(html, _subtype='html', _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print "发送成功", msg_to
        s.quit()
        return 1
    except:
        print "发现异常！！！！！！！！！！！！！"
        print msg_to
        return 0


today = datetime.date.today()
today_0 = today + datetime.timedelta(days=-1)
week = []
for i in range(1, 31):
    t = today + datetime.timedelta(days=-i)
    week.append(t)
mail = []   # 邮件内容
hostid = gethostid_avg()
for host in hostid:
    
    data_week = []  # 保存取出来的数据
    # 将数据添加到data_week中
    i = 0
    while i < 30:
        data_week.append(get_avg(host, week[i]))
        i = i + 1
    i = 1
    k = 0
    cpu_ch = 0.0
    mem_ch = 0.0
    disk_ch = 0.0
    #计算三十天累计变动值
    try:
	
        while i < 30:
            cpu_ch = cpu_ch + data_week[i][0] - data_week[k][0]
            mem_ch = mem_ch + data_week[i][1] - data_week[k][1]
            disk_ch = disk_ch + data_week[i][2] - data_week[k][2]
            i = i + 1
            k = k + 1
    except:
	cpu_ch = 0.0
	mem_ch = 0.0
	disk_ch = 0.0
	print host,"lack of data!"
    if data_week[k][1] :
	mem_ch_per = mem_ch / data_week[k][1] * 100
    else :
	mem_ch_per = 0
    #mem_ch_per = data_week[k][1] / (mem_ch + 1)
    #设定报警的波动值
    name = str(gethostname(host))
    try:
        if (cpu_ch > 8 and data_week[k][0] <90) or (mem_ch_per > 10 ) or (disk_ch > 8):
	    total = gettotalmem(host)
            mail.append((name,round(100-data_week[29][0],1),round(100-data_week[0][0],1),round(cpu_ch,1),\
	    round((total-data_week[29][1])/1073741824.00,2),round((total -data_week[0][1])/1073741824.00,2),round(float(data_week[29][1]-data_week[0][1])/(total-data_week[29][1])*100,2),\
	    round(total/1073741824.00,2),round(100-data_week[29][2],2),round(100-data_week[0][2],2),\
	    round(disk_ch,2)))
	    print name,cpu_ch,mem_ch_per,disk_ch
        else:
            print host,"正 常"
            print name,cpu_ch,mem_ch_per,disk_ch
    except Exception ,e:
	print str(e.message)
	mail.append((host,"异 常"))
	print host,name,"异 常"

if mail:
    send_msg('op@roobo.com',mail)
    
else:
    print "all device is normal !"




