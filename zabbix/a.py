#/usr/bin/python2.7
#encoding:utf-8

import MySQLdb


def gethostid():
    hostid = []
    #db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix")
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","zabbix" )
    cursor = db.cursor()
    sql = "select hostid,host,status from hosts where hostid > 10100 and status=0 order by hostid;"
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


def insert(hostname):
    db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor" )
    cursor = db.cursor()
    sql = "insert into host (hostname, username) select '" + str(hostname) + "', 'huxiaolong' from dual where not exists (select * from host where host.hostname = '" + str(hostname) + "' and username = 'huxiaolong');"
    cursor.execute(sql)
    db.commit()
    db.close()



hosts = ['ai-templatees02-01','ai-templatees02-02','ai-templatees02-03','ai-templatees02-04']
usernames = []
db = MySQLdb.connect("10.44.13.30","zabbix","zabbix","monitor" )
cursor = db.cursor()
for host in hosts:
    usernames = []
    host0 = host[:-5]
    sql = "select distinct username from host where hostname like '" + host0 + "%';"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        usernames.append(cur1[0])
        cur1 = cursor.fetchone()
    usernames = ['huxiaolong','sungaomeng']
    for username in usernames:
	sql = "insert into host values('"+ host + "','"+ username + "');"
	print sql
	cursor.execute(sql)
db.commit()
db.close()
