#!/usr/bin/python
# -*- coding: latin-1 -*-

import matplotlib.pyplot as plt
import time
#from ngsimu import *
import pickle



def load_graph(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempgr=mon_depickler.load()
	return tempgr

def merge_meanstd():
	pass

class CustomGraph(object):
	def __init__(self,Y,*arg,**kwargs):

		self.filename="graph"+time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.title=self.filename
		self.xlabel="X"
		self.ylabel="Y"

		self.Yoptions=[{}]

		self.xmin=[0,0]
		self.xmax=[0,5]
		self.ymin=[0,0]
		self.ymax=[0,5]
		
		
		self._Y=[Y]
		if len(arg)!=0:
			self._X=[arg[0]]
		else:
			self._X=[range(0,len(Y))]


		self.extensions=["eps","png"]

		for key,value in kwargs.iteritems():
			setattr(self,key,value)


		if not isinstance(self.xmin,list):
			temp=self.xmin
			self.xmin=[1,temp]
		if not isinstance(self.xmax,list):
			temp=self.xmax
			self.xmax=[1,temp]
		if not isinstance(self.ymin,list):
			temp=self.ymin
			self.ymin=[1,temp]
		if not isinstance(self.ymax,list):
			temp=self.ymax
			self.ymax=[1,temp]


	def show(self):
		self.draw()
		plt.ion()
		plt.show()

	def save(self):
		with open(self.filename+".b", 'wb') as fichier:
			mon_pickler=pickle.Pickler(fichier)
			mon_pickler.dump(self)

	def write_files(self):
		self.draw()
		self.save()
		for extension in self.extensions:
			plt.savefig(self.filename+"."+extension,format=extension)


	def draw(self):
		plt.figure()
		plt.cla()
		plt.clf()
		for i in range(0,len(self._Y)): 
			plt.plot(self._X[i],self._Y[i],**self.Yoptions[i])
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		plt.title(self.title)

		if self.xmin[0]:
			plt.xlim(xmin=self.xmin[0])
		if self.xmax[0]:
			plt.xlim(xmax=self.xmax[0])
		if self.ymin[0]:
			plt.ylim(xmin=self.ymin[0])
		if self.ymax[0]:
			plt.ylim(xmax=self.ymax[0])
		plt.legend()
		plt.draw()


	def add_graph(self,other_graph):
		self._X=self._X+other_graph._X
		self._Y=self._Y+other_graph._Y





