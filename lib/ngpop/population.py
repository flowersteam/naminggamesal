#!/usr/bin/python
# -*- coding: latin-1 -*-

#import random
#from ngvoc import *
import os
from copy import deepcopy
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt

from ..ngagent_2 import Agent



class Population(object):
#	def deepcopy(self):
#		filename="temppop"+str(os.getpid())+".tmp"
#		with open(filename, 'wb') as fichier:
#			mon_pickler = pickle.Pickler(fichier)
#			mon_pickler.dump(self)
#		with open(filename, 'rb') as fichier:
#			mon_depickler = pickle.Unpickler(fichier)
#			pop_recup = mon_depickler.load()
#		os.remove(filename)
#		return pop_recup


	def __init__(self, voc_cfg, strat_cfg, nbagent):
		self._size = 0
		self._voc_cfg = voc_cfg
		self._M=voc_cfg['M']
		self._W=voc_cfg['W']
		self._strat_cfg=strat_cfg
		self._lastgameinfo=[]
		self._agentlist=[]
		for i in range (0,nbagent):
			self.add_new_agent(agent_id=i, strat_cfg=strat_cfg, voc_cfg=voc_cfg)


	def get_size(self):
		return self._size
	def get_vocsize(self):
		return [self._M,self._W]
	def check_id(self,agent_id):
		for i in range(0,len(self._agentlist)):
			if self._agentlist[i].get_id()==agent_id:
				return 1
		return 0
	def add_agent(self,agent):
		if self.check_id(agent.get_id())==1:
			print "ATTENTION: 2 agents avec la même identité"
		self._agentlist.append(agent)

	def idmax(self): #Suppose ID=nombre
		tempid=0
		for i in range(0,len(self._agentlist)):
			tempid=max(tempid,self._agentlist[i].get_id())
		return tempid

	def add_new_agent(self, voc_cfg, strat_cfg, agent_id=None):
		if agent_id is not None:
			agent_id=self.idmax()+1
		self._agentlist.append(Agent(agent_id=agent_id, voc_cfg=self._voc_cfg, strat_cfg=self._strat_cfg))
		self._size+=1

	def get_index_from_id(self,agent_id):
		for i in range (0,len(self._agentlist)):
			if self._agentlist[i].get_id()==agent_id:
				return i
		print "id non existante"

	def rm_agent(self,agent_id):
		self._agentlist.remove(self.get_index_from_id(agent_id))
		self._size-=1

	def pick_speaker(self):
		j=random.randint(0,len(self._agentlist)-1)
 		return self._agentlist[j].get_id()

	def pick_hearer(self,speaker_id):
		j=random.randint(0,len(self._agentlist)-2)
		if self.get_index_from_id(speaker_id) <= j:
			j+=1
 		return self._agentlist[j].get_id()

	def play_game(self,steps,**kwargs):
		for i in range(0,steps):
			speaker_id=self.pick_speaker()
			hearer_id=self.pick_hearer(speaker_id)
			speaker=self._agentlist[self.get_index_from_id(speaker_id)]
			hearer=self._agentlist[self.get_index_from_id(hearer_id)]
			tempmw=speaker.pick_mw()
			ms=tempmw[0]
			w=tempmw[1]
			mh=hearer.guess_m(w)
			if ms==mh:
				speaker.success+=1
				hearer.success+=1
			else:
				speaker.fail+=1
				hearer.fail+=1
			speaker.update_speaker(ms,w,mh)
			hearer.update_hearer(ms,w,mh)
			self._lastgameinfo=[ms,w,mh,speaker_id,hearer_id]

	def get_lastgameinfo(self):
		return self._lastgameinfo

	def reconstruct_from_info(self,game_info):
		ms=game_info[0]
		w=game_info[1]
		mh=game_info[2]
		sp_id=game_info[3]
		hr_id=game_info[4]
		speaker=self._agentlist[self.get_index_from_id(sp_id)]
		hearer=self._agentlist[self.get_index_from_id(hr_id)]
		if ms==mh:
			speaker.success+=1
			hearer.success+=1
		else:
			speaker.fail+=1
			hearer.fail+=1
		speaker.update_speaker(ms,w,mh)
		hearer.update_hearer(ms,w,mh)
		self._lastgameinfo=[ms,w,mh,sp_id,hr_id]


	def sort_agentlist(self):
		def tempfun(agent):
			return agent.get_id()
		self._agentlist.sort(tempfun)

	def __str__(self):
		return self.repr()

	def repr(self,*args):
		tempstr = ""
		if len(args)==0:
			tempstr += "nbagent: "+str(self._size)+"\n"
			temprep=np.matrix(np.zeros((self._M,self._W)))
			for i in range(0,self._size):
				temprep=temprep+self._agentlist[i].get_vocabulary_content()
			tempstr += str(temprep/self._size)
		elif args[0]=="all":
			for i in range(0,self._size):
				tempstr += "Agent ID: "+str(self._agentlist[i].get_id())+"\n"
				tempstr += str(self._agentlist[i])
				tempstr += "\n"
		else:
			i=self.get_index_from_id(args[0])
			tempstr+="Agent ID: "+str(args)
			tempstr+=str(self._agentlist[i])
		return tempstr

	def visual(self,vtype=None,ag_list=None):
		tempstr = ""
		if ag_list==None or ag_list=="all":
			ag_list=range(0,len(self._agentlist))
		if vtype==None:
			tempstr += "nbagent: "+str(self._size)+"\n"
			temprep=np.matrix(np.zeros((self._M,self._W)))
			for i in ag_list:
				temprep=temprep+self._agentlist[i].get_vocabulary_content()
			plt.figure()
			plt.title("Average on Population")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(temprep/self._size),vmin=0,vmax=1)
		else:
			if vtype=="agents":
				vtype=None
			for i in ag_list:
				print("Agent ID: "+str(self._agentlist[i].get_id())+"\n")
				self._agentlist[i].visual(vtype=vtype)
				print("\n")

	def get_content(self,*args):
		if len(args)==0:
			temprep=np.matrix(np.zeros((self._M,self._W)))
			for i in range(0,self._size):
				temprep=temprep+self._agentlist[i].get_vocabulary_content()
			return temprep/self._size
		elif args[0]=="all":
			temprep=[]
			for i in range(0,self._size):
				temprep.append(self._agentlist[i].get_vocabulary_content())
			return temprep
		else:
			i=self.get_index_from_id(args[0])
			print "Agent ID: %s" %args
			print str(self._agentlist[i])




if __name__ == "__main__":
	testpop=ngagent.Population("matrix","naive",10,12,15)
