#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client    #客户类，其实叫account感觉更加合理，因为它是维护accessKeyId和secretKeyId的对象
from aliyunsdkcms.request.v20170301 import QueryMetricListRequest    #QueryMetricList是阿里云方面规定的一个名字，意思是要获取多条监控数据的请求
import json


class rooboaliyun:
    #连接key
    access_key = ''
    secret_key = ''
    region_id = ''
    clt = client.AcsClient('', '', '')

    #获取全部实例id

    #获取指定id的特定性能参数cpu、内存、磁盘、tcp、io、
    #获取一天内CPU使用率中60个1分钟均值的峰值点的均值
    def get_cpu(self,instanceID,date):

        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('JSON')
        request.set_Project('acs_kvstore')
        request.set_Metric('CpuUsage')
        request.set_StartTime(str(date) + ' 00:00:00')
        request.set_EndTime(str(date) + ' 23:59:00')
        request.set_Dimensions("{'instanceId':'" + instanceID + "'}")
        request.set_Period('60')

        res = json.loads(self.clt.do_action_with_exception(request))

        average_value = []
        for point in res['Datapoints']:
            average_value.append(point['Average'])
        average_sorted = sorted(average_value, reverse=True)
        average = 0.0
        try:
            for i in range(0, 60):
                average = average + average_sorted[i]
            average = average / 60
        except:
            average = 99.99
        return average
    #获取前一天所有值，并取峰值60分钟的均值

    def get_mem(self,instanceID,date):

        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('JSON')
        request.set_Project('acs_kvstore')
        request.set_Metric('MemoryUsage')
        request.set_StartTime(str(date) + ' 00:00:00')
        request.set_EndTime(str(date) + ' 23:59:00')
        request.set_Dimensions("{'instanceId':'" + instanceID + "'}")
        request.set_Period('60')

        res = json.loads(self.clt.do_action_with_exception(request))

        average_value = []
        for point in res['Datapoints']:
            average_value.append(point['Average'])
        average_sorted = sorted(average_value, reverse=True)
        average = 0.0
        try:
            for i in range(0, 60):
                average = average + average_sorted[i]
            average = average / 60
        except:
            average = 99.99
        return average

    def get_in(self,instanceID,date):

        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('JSON')
        request.set_Project('acs_kvstore')
        request.set_Metric('IntranetInRatio')
        request.set_StartTime(str(date) + ' 00:00:00')
        request.set_EndTime(str(date) + ' 23:59:00')
        request.set_Dimensions("{'instanceId':'" + instanceID + "'}")
        request.set_Period('60')

        res = json.loads(self.clt.do_action_with_exception(request))

        average_value = []
        for point in res['Datapoints']:
            average_value.append(point['Average'])
        average_sorted = sorted(average_value, reverse=True)
        average = 0.0
        try:
            for i in range(0, 60):
                average = average + average_sorted[i]
            average = average / 60
        except:
            average = 99.99
        return average

    def get_out(self,instanceID,date):

        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('JSON')
        request.set_Project('acs_kvstore')
        request.set_Metric('IntranetOutRatio')
        request.set_StartTime(str(date) + ' 00:00:00')
        request.set_EndTime(str(date) + ' 23:59:00')
        request.set_Dimensions("{'instanceId':'" + instanceID + "'}")
        request.set_Period('60')

        res = json.loads(self.clt.do_action_with_exception(request))

        average_value = []
        for point in res['Datapoints']:
            average_value.append(point['Average'])
        average_sorted = sorted(average_value, reverse=True)
        average = 0.0
        try:
            for i in range(0, 60):
                average = average + average_sorted[i]
            average = average / 60
        except:
            average = 99.99
        return average

