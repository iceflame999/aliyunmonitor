# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class CreateAlarmRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Cms', '2017-03-01', 'CreateAlarm','cms')
		self.set_method('POST')

	def get_callby_cms_owner(self):
		return self.get_query_params().get('callby_cms_owner')

	def set_callby_cms_owner(self,callby_cms_owner):
		self.add_query_param('callby_cms_owner',callby_cms_owner)

	def get_Name(self):
		return self.get_query_params().get('Name')

	def set_Name(self,Name):
		self.add_query_param('Name',Name)

	def get_Namespace(self):
		return self.get_query_params().get('Namespace')

	def set_Namespace(self,Namespace):
		self.add_query_param('Namespace',Namespace)

	def get_MetricName(self):
		return self.get_query_params().get('MetricName')

	def set_MetricName(self,MetricName):
		self.add_query_param('MetricName',MetricName)

	def get_Dimensions(self):
		return self.get_query_params().get('Dimensions')

	def set_Dimensions(self,Dimensions):
		self.add_query_param('Dimensions',Dimensions)

	def get_Period(self):
		return self.get_query_params().get('Period')

	def set_Period(self,Period):
		self.add_query_param('Period',Period)

	def get_Statistics(self):
		return self.get_query_params().get('Statistics')

	def set_Statistics(self,Statistics):
		self.add_query_param('Statistics',Statistics)

	def get_ComparisonOperator(self):
		return self.get_query_params().get('ComparisonOperator')

	def set_ComparisonOperator(self,ComparisonOperator):
		self.add_query_param('ComparisonOperator',ComparisonOperator)

	def get_Threshold(self):
		return self.get_query_params().get('Threshold')

	def set_Threshold(self,Threshold):
		self.add_query_param('Threshold',Threshold)

	def get_EvaluationCount(self):
		return self.get_query_params().get('EvaluationCount')

	def set_EvaluationCount(self,EvaluationCount):
		self.add_query_param('EvaluationCount',EvaluationCount)

	def get_ContactGroups(self):
		return self.get_query_params().get('ContactGroups')

	def set_ContactGroups(self,ContactGroups):
		self.add_query_param('ContactGroups',ContactGroups)

	def get_StartTime(self):
		return self.get_query_params().get('StartTime')

	def set_StartTime(self,StartTime):
		self.add_query_param('StartTime',StartTime)

	def get_EndTime(self):
		return self.get_query_params().get('EndTime')

	def set_EndTime(self,EndTime):
		self.add_query_param('EndTime',EndTime)

	def get_SilenceTime(self):
		return self.get_query_params().get('SilenceTime')

	def set_SilenceTime(self,SilenceTime):
		self.add_query_param('SilenceTime',SilenceTime)

	def get_NotifyType(self):
		return self.get_query_params().get('NotifyType')

	def set_NotifyType(self,NotifyType):
		self.add_query_param('NotifyType',NotifyType)