#!/usr/bin/python
# -*- coding: latin-1 -*-

import matplotlib.pyplot as plt
import time
import numpy as np
import pickle


plt.ion()

def load_graph(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempgr=mon_depickler.load()
	return tempgr


class CustomGraph(object):
	def __init__(self,Y,*arg,**kwargs):
		self.sort=1
		self.filename="graph"+time.strftime("%Y%m%d%H%M%S", time.localtime())
		if "filename" in kwargs.keys():
			self.filename=kwargs["filename"]
		self.title=self.filename
		self.xlabel="X"
		self.ylabel="Y"
		self.alpha=0.3

		self.Yoptions=[{}]

		self.xmin=[0,0]
		self.xmax=[0,5]
		self.ymin=[0,0]
		self.ymax=[0,5]
		
		self.std=0
		
		self._Y=[Y]
		self.stdvec=[0]*len(Y)

		if len(arg)!=0:
			self._X=[Y]
			self._Y=[arg[0]]
		else:
			self._X=[range(0,len(Y))]


		self.extensions=["eps","png"]

		for key,value in kwargs.iteritems():
			setattr(self,key,value)

		self.stdvec=[self.stdvec]

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
		plt.figure()
		self.draw()
		#plt.show()

	def save(self,*path):
		if len(path)!=0:
			out_path=path[0]
		else:
			out_path=""
		with open(out_path+self.filename+".b", 'wb') as fichier:
			mon_pickler=pickle.Pickler(fichier)
			mon_pickler.dump(self)

	def write_files(self,*path):
		if len(path)!=0:
			out_path=path[0]
		else:
			out_path=""

		self.draw()
		self.save(out_path)
		for extension in self.extensions:
			plt.savefig(out_path+self.filename+"."+extension,format=extension)


	def draw(self):
		#plt.figure()
		plt.cla()
		plt.clf()
		for i in range(0,len(self._Y)): 

			Xtemp=self._X[i]
			Ytemp=self._Y[i]
			if self.sort:
				tempdic={}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=Ytemp[j]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					Ytemp[j]=temptup[j][1]

			Xtemp=self._X[i]
			stdtemp=self.stdvec[i]
			if self.sort:
				tempdic={}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=stdtemp[j]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					stdtemp[j]=temptup[j][1]
			if self.std:
				Ytempmin=[0]*len(Ytemp)
				Ytempmax=[0]*len(Ytemp)
				for j in range(0,len(Ytemp)):
					Ytempmax[j]=Ytemp[j]+stdtemp[j]
					Ytempmin[j]=Ytemp[j]-stdtemp[j]
				plt.fill_between(Xtemp,Ytempmin,Ytempmax,alpha=self.alpha,**self.Yoptions[i])
			plt.plot(Xtemp,Ytemp,**self.Yoptions[i])
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		plt.title(self.title)

		if self.xmin[0]:
			plt.xlim(xmin=self.xmin[1])
		if self.xmax[0]:
			plt.xlim(xmax=self.xmax[1])
		if self.ymin[0]:
			plt.ylim(ymin=self.ymin[1])
		if self.ymax[0]:
			plt.ylim(xmax=self.ymax[1])
		plt.legend()
		plt.draw()


	def add_graph(self,other_graph):
		self._X=self._X+other_graph._X
		self._Y=self._Y+other_graph._Y
		self.Yoptions=self.Yoptions+other_graph.Yoptions
		self.stdvec=self.stdvec+other_graph.stdvec

	def merge(self):
		Yarray=np.array(self._Y)
		stdarray=np.array(self.stdvec)
		stdtemp=[]
		Ytemp=[]

		for i in range(0,len(self._Y[0])):
			Ytemp.append(np.mean(list(Yarray[:,i])))
			stdtemp.append(np.std(list(Yarray[:,i])))
		self._Y=[Ytemp]
		self.stdvec=[stdtemp]
		self._X=[self._X[0]]




