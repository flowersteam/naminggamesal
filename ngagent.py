#!/usr/bin/python
# -*- coding: latin-1 -*-

import random

class Agent(object):
	def __init__(self,strattype,voctype,agent_id):
		self._id=agent_id;
		self._vocabulary=
		self._strategy=Strategy(strattype)
		self.init_memory()

	def get_voctype(self):
		self._vocabulary.get_voctype()

	def get_id(self):
		return self._id

	def affiche(self):
		self._vocabulary.affiche()

	def pick_mw(self):
		self._strategy.pick_mw(self._vocabulary,self._memory)

	def pick_new_m(self):
		self._strategy.pick_new_m(self._vocabulary,self._memory)

	def guess_m(self,w):
		self._strategy.guess_m(w,self._vocabulary,self._memory)

	def pick_w(self,m):
		self._strategy.pick_w(m,self._vocabulary,self._memory)

	def update_hearer(self,ms,w,mh):
		self._strategy.update_hearer(self._vocabulary,self._memory)

	def update_speaker(self,ms,w,mh):
		self._strategy.update_speaker(self._vocabulary,self._memory)

	def init_memory(self):
		self._strategy.init_memory(self._vocabulary)

class Population(object):
	def __init__(self,voctype,strattype,nbagents,M,W):
		self._size=nbagents
		self._voctype=voctype
		self._M=M
		self._W=W
		self._strattype=strattype
		self._lastgameinfo=[]
		self._agentlist=[]
		for i in range (0,self._size):
			_agentlist.append(self.add_new_agent(self._voctype,self._strattype,i))


	def get_size(self):
		return self._size
	def get_vocsize(self):
		return [self._M,self._W]
	def check_id(self,agent_id):
		for i in range(0,self._agentlist.length()):
			if self._agentlist[i].get_id()==agent_id:
				return 1
		return 0
	def add_agent(self,agent):
		if self.check_id(agent.get_id())==1:
			print "ATTENTION: 2 agents avec la même identité"
		self._agentlist.append(agent)

	def idmax(self): #Suppose ID=nombre
		tempid=0
		for i in range(0,self._agentlist.length()):
			tempid=max(tempid,self._agentlist[i].get_id())
		return tempid

	def add_new_agent(self,voctype,strattype,*args):
		if args.length()!=0:
			agent_id=args[0]
		else:
			agent_id=self.idmax()+1
		self._agent_list.append(Agent(strattype,voctype,agent_id))

	def get_index_from_id(self,agent_id):
		for i in range (0,self._agentlist.length()):
			if self._agentlist[i]==agent_id:
				return i
		print "id non existante"

	def rm_agent(self,agent_id):
		self._agentlist.remove(self.get_index_from_id(agent_id))

	def pick_speaker(self):
		j=random.randint(0,self._agentlist.length()-1)
 		return self._agentlist[j].get_id()

	def pick_hearer(self,speaker_id):
		j=random.randint(0,self._agentlist.length()-2)
		if self.get_index_from_id(speaker_id)<=j
			j+=1
 		return self._agentlist[j].get_id()

	def play_game(self):
		speaker_id=self.pick_speaker()
		hearer_id=self.pick_hearer(speaker_id)
		speaker=self._agentlist[self.get_index_from_id(speaker_id)]
		hearer=self._agentlist[self.get_index_from_id(hearer_id)]
		[ms,w]=speaker.pick_mw()
		mh=hearer.guess_m(w)
		speaker.update_speaker(ms,w,mh)
		hearer.update_hearer(ms,w,mh)
		self._lastgameinfo=[ms,w,mh]

	def get_lastgameinfo(self):
		return self._lastgameinfo

	def sort_agentlist(self):
		def tempfun(agent):
			return agent.get_id()
		self._agentlist.sort(tempfun)

