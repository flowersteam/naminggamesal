#!/usr/bin/python
# -*- coding: latin-1 -*-

import copy

class CustomFunc(object):

	def __init__(self,func,level=None,tags=None,**kwargs):
		self.level = level
		if tags is None:
			self.tags = []
		elif isinstance(tags,list):
			self.tags = copy.deepcopy(tags)
		else:
			self.tags = [copy.deepcopy(tags)]

		def dataname(data):
			out = ""
			try:
				out = data.__name__
			except AttributeError:
				pass
			return out

		def yname(data):
			out=""
			try:
				out=func.__name__+"("+data.__name__+")"
			except AttributeError:
				pass
			return out

		self.func = func
		self.graph_config={"xlabel":dataname,"ylabel":yname}
		for key, value in kwargs.items():
			self.graph_config[key]=value
		self.graph_config_temp={}
		#self.graph_config_temp=copy.deepcopy(self.graph_config)

	def apply(self,data,**kwargs):
		for key,value in self.graph_config.items():
			if value(data) is not None:
				self.graph_config_temp[key]=value(data)
		if "progress_info" in list(kwargs.keys()):
			return self.func(data,progress_info=kwargs["progress_info"])
		return self.func(data)

	def modify_graph_config(self,**kwargs):
		tempcfg=self.graph_config_temp
		for key, value in kwargs.items():
			self.graph_config_temp[key]=value


	def get_graph_config(self):
		return self.graph_config_temp
