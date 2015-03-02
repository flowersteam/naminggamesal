#!/usr/bin/python
# -*- coding: latin-1 -*-


import os

class Tmsu:

	def __init__(self,**kwargs):
		for key, value in kwargs.iteritems():    
			setattr(self, key, value)

	def tag(self,**kwargs):
		filepathandname=kwargs["filename"]
		filepathandname=os.popen("readlink -f "+filepathandname, "r").read()
		filepathandname=filepathandname[:-1]
		command="tmsu --database "+self.dbpath+" tag "+filepathandname
		for temptag in kwargs["tags"]:
			command=command+" "+temptag
		os.system(command)


	def untag(self,**kwargs):
		filepathandname=kwargs["filename"]
		filepathandname=os.popen("readlink -f "+filepathandname, "r").read()
		filepathandname=filepathandname[:-1]
		command="tmsu --database "+self.dbpath+" untag "+filepathandname
		for temptag in kwargs["tags"]:
			command=command+" "+temptag
		os.system(command)

	def get_tags(self,**kwargs):
		filepathandname=kwargs["filename"]
		filepathandname=os.popen("readlink -f "+filepathandname, "r").read()
		filepathandname=filepathandname[:-1]	
		command="tmsu --database "+self.dbpath+" tags "+filepathandname
		tempstr=os.popen(command, "r").read()
		return tempstr[len(kwargs["filename"])+1:-1]

	def get_tags_list(self,**kwargs):
		return self.get_tags(**kwargs).split(' ')