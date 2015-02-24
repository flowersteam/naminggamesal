#!/usr/bin/python
# -*- coding: latin-1 -*-

import time
import pickle
from ngagent import *
from copy import deepcopy

def load_experiment(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempexp=mon_depickler.load()
	return tempexp

class Experiment(object):

	def __init__(self,voctype,strattype,M,W,nbagent,step):
		self._voctype=voctype
		self._strattype=strattype
		self._M=M
		self._W=W
		self._nbagent=nbagent
		self._time_step=step
		self._T=[]
		self._poplist=[]
		self.add_pop(Population(voctype,strattype,M,W,nbagent),0)



	def affiche(self):
		print "T: %i" %self._T[-1]
		self._poplist[-1].affiche()
	
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


	def continue_exp(self,T,*progress_info):
		temppop=self.get_pop("last")
		temptmax=self._T[-1]
		while temptmax <T :
			if len(progress_info)!=0:
				progress_info_2=(progress_info[0]+" T:"+str(temptmax)+"/"+str(T),)
			temppop.play_game(self._time_step,*progress_info_2)
			self.add_pop(temppop.deepcopy(),self._T[-1]+self._time_step)
			temptmax+=self._time_step

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




