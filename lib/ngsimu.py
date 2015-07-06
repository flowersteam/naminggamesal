#!/usr/bin/python
# -*- coding: latin-1 -*-

import time
import pickle
from ngagent import *
from copy import deepcopy
import ngmeth
import additional.custom_func as custom_func
import additional.custom_graph as custom_graph
import uuid

def load_experiment(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempexp=mon_depickler.load()
	return tempexp

class Experiment(object):

	def __init__(self,voctype="sparse",strat={"strattype":"naive"},M=5,W=5,nbagent=10,step=1):
		self._voctype=voctype
		self._strat=strat
		self._M=M
		self._W=W
		self._nbagent=nbagent
		self._time_step=step
		self._T=[]
		self._poplist=[]
		self.add_pop(Population(voctype=voctype,strat=strat,nbagent=nbagent,M=M,W=W),0)
		self.uuid=str(uuid.uuid1())
		self.init_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.reconstruct_info=[]



	def __str__(self):
		return "T: "+str(self._T[-1])+"\n"+str(self._poplist[-1])

	def get_self(self):
		return self

	def save(self,filename):
		with open(filename,'wb') as fichier:
			testpickler=pickle.Pickler(fichier)
			testpickler.dump(self.get_self())

	def get_pop(self,tempindex):
		if tempindex=="last":
			return self._poplist[-1].deepcopy()
		return self._poplist[tempindex].deepcopy()


	def continue_exp_until(self,T,**kwargs):
		temppop=self.get_pop("last")
		temptmax=self._T[-1]
		while temptmax <T :
			if "progress_info" in kwargs.keys():
				progress_info_2=kwargs["progress_info"]+" T:"+str(temptmax)+"/"+str(T)
				for tt in range(0,self._time_step):
					temppop.play_game(1,progress_info=progress_info_2)
					self.reconstruct_info.append(temppop._lastgameinfo)
			else:
				for tt in range(0,self._time_step):
					temppop.play_game(self._time_step)
					self.reconstruct_info.append(temppop._lastgameinfo)
			self.add_pop(temppop.deepcopy(),self._T[-1]+self._time_step)
			temptmax+=self._time_step
			self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
#		if self._T[-1]!=T:
#			if len(progress_info)!=0:
#				progress_info_2=(progress_info[0]+" T:"+str(T-1)+"/"+str(T),)
#			temppop.play_game(T-self._T[-1],*progress_info_2)
#			self.add_pop(temppop.deepcopy(),T)

	def continue_exp(self,dT,**kwargs):
		self.continue_exp_until(self._T[-1]+dT,**kwargs)

	def add_pop(self,pop,T):
		self._poplist.append(pop)
		self._T.append(T)

	def extend_step(self,bigstep):
		tempt=self._T[0]
		temppoplist=[self._poplist[0]]
		tempT=[self._T[0]]
		for i in range(1,len(self._T)):
			if self._T[i]>=tempt+bigstep:
				temppoplist.append(self.get_pop(i))
				tempT.append(self._T[i])
				tempt=self._T[i]
		self._T=tempT
		self._poplist=temppoplist

	def set_time_step(self,newstep):
		self._time_step=newstep

	def truncate(self,tmax):
		while self._T[-1]>tmax:
			self._poplist.pop()
			self._T.pop()

	def visual(self,vtype=None,ag_list=None,tmax=None):
		if tmax==None:
			tmax=self._T[-1]
		ind=-1
		while self._T[ind]>tmax:
			ind-=1
		self._poplist[ind].visual(vtype=vtype,ag_list=ag_list)

	def graph(self,method="srtheo",X=None,tmin=0,tmax=None):
		if not tmax:
			tmax=self._T[-1]
		indmax=-1
		while self._T[indmax]>tmax:
			indmax-=1
		indmin=0
		while self._T[indmin]<tmin:
			indmin+=1
		tempfun=getattr(ngmeth,"custom_"+method)
		tempoutmean=[]
		tempoutstd=[]
		if tempfun.level=="agent":
			for j in range(indmin,len(self._poplist)+1+indmax):
				tempout=tempfun.apply(self._poplist[j])
				tempoutmean.append(tempout[0])
				tempoutstd.append(tempout[1])
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempoutmean
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			stdvec=tempoutstd
			tempgraph=custom_graph.CustomGraph(tempX,tempY,std=1,sort=0,stdvec=stdvec,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="population":
			tempout=[]
			for j in range(indmin,len(self._poplist)+1+indmax):
				tempout.append(tempfun.apply(self._poplist[j]))
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempout
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			tempgraph=custom_graph.CustomGraph(tempX,tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="time":
			tempout=tempfun.apply(self)
			tempout=tempout[indmin:(len(self._T)+indmax+1)]
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempout
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			tempgraph=custom_graph.CustomGraph(tempX,tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		else:
			print("Custom_func level doesn't exist or has an unknown value:")
			print(tempfun.level)
		if X:
			tempgraph2=self.graph(method=X,tmin=tmin,tmax=tmax)
			tempgraph=tempgraph.func_of(tempgraph2)
		return tempgraph



