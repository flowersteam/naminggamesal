#!/usr/bin/python
# -*- coding: latin-1 -*-

import copy

class CustomFunc(object):

	def __init__(self,func,*level,**kwargs):
		if len(level)!=0:
			self.level=level[0]

		self.func=func
		self.graph_config={"xlabel":"","ylabel":func.__name__}
		for key, value in kwargs.iteritems():
			self.graph_config[key]=value
		self.graph_config_temp=copy.deepcopy(self.graph_config)

	def apply(self,data,*progress_info):
		self.graph_config_temp=copy.deepcopy(self.graph_config)
		if self.graph_config["xlabel"]=="":
			try:
				self.graph_config_temp["xlabel"]=data.__name__
			except AttributeError:
				pass
		if self.graph_config["ylabel"]==self.func.__name__:
			try:
				self.graph_config_temp["ylabel"]=self.func.__name__+"("+data.__name__+")"
			except AttributeError:
				pass
		if len(progress_info)!=0:
			return self.func(data,progress_info[0])
		return self.func(data)

	def modify_graph_config(self,**kwargs):
		tempcfg=self.graph_config_temp
		for key, value in kwargs.iteritems():
			self.graph_config_temp[key]=value

	def get_graph_config(self):
		return self.graph_config_temp


