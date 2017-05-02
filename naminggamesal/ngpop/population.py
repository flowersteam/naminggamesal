#!/usr/bin/python

#import random
#from ngvoc import *
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import uuid
import copy

from ..ngagent import Agent
from ..nginter import get_interaction
from ..ngtopology import get_topology
from ..ngenv import get_environment
from ..ngagentpicking import get_agentpick
from ..ngevol import get_evolution



class Population(object):

	def __init__(self, voc_cfg, strat_cfg, interact_cfg, nbagent, evolution_cfg={'evolution_type':'idle'}, agentpick_cfg={'agentpick_type':'random_pick'}, sensor_cfg=None, env_cfg=None,topology_cfg={'topology_type':'full_graph'}):
		self._size = 0
		self._voc_cfg = voc_cfg
		if 'M' in voc_cfg.keys():
			self._M = voc_cfg['M']
			self._W = voc_cfg['W']
		elif 'subvoc_cfg' in voc_cfg.keys() and 'M' in voc_cfg['subvoc_cfg'].keys():
			self._M = voc_cfg['subvoc_cfg']['M']
			self._W = voc_cfg['subvoc_cfg']['W']
		self._strat_cfg = strat_cfg
		self._agentpick_cfg = agentpick_cfg
		self.agent_pick = get_agentpick(**agentpick_cfg)
		self._sensor_cfg = sensor_cfg
		self._env_cfg = env_cfg
		self._interaction = get_interaction(**interact_cfg)
		self._evolution = get_evolution(**evolution_cfg)
		if env_cfg is None:
			self.env = None
		else:
			if 'uuid_instance' not in self._env_cfg.keys():
				self.env_id = str(uuid.uuid1())
			else:
				self.env_id = self._env_cfg['uuid_instance']
			self.env = get_environment(uuid_instance=self.env_id,**self._env_cfg)
		self._lastgameinfo = []
		self._past = []
		self._agentlist = []
		for i in range(nbagent):
			self.add_new_agent(agent_id=None, strat_cfg=strat_cfg, voc_cfg=voc_cfg, sensor_cfg=sensor_cfg)
		self._topology = get_topology(pop=self,**topology_cfg)


	def get_size(self):
		return self._size

	def get_vocsize(self):
		return [self._M,self._W]

	def check_id(self,agent_id):
		for i in range(0,len(self._agentlist)):
			if self._agentlist[i].get_id() == agent_id:
				return 1
		return 0

	def add_agent(self, agent):
		if self.check_id(agent.get_id()) == 1:
			print "WARNING: 2 agents with same identity"
		self._agentlist.append(agent)
		self._size+=1
		if hasattr(self,'_topology'):
			self._topology.add_agent(agent,pop=self)

	def idmax(self): #Suppose ID=nombre
		tempid=0
		for i in range(0,len(self._agentlist)):
			tempid=max(tempid,self._agentlist[i].get_id())
		return tempid

	def add_new_agent(self, voc_cfg=None, strat_cfg=None, sensor_cfg=None, agent_id=None):
		if voc_cfg is None:
			voc_cfg = self._voc_cfg
		if strat_cfg is None:
			strat_cfg = self._strat_cfg
		if sensor_cfg is None:
			sensor_cfg = self._sensor_cfg
		agent = Agent(voc_cfg=voc_cfg, strat_cfg=strat_cfg, sensor_cfg=sensor_cfg, agent_id=agent_id, env=self.env)
		self.add_agent(agent)

	def get_index_from_id(self, agent_id):
		for i in range (0,len(self._agentlist)):
			if self._agentlist[i].get_id() == agent_id:
				return i
		print "id non existante"

	def rm_agent(self, agent_id=None):
		if agent_id is None:
			agent = self._agentlist[0]
			agent_id =  agent._id
		else:
			agent = self._agentlist[self.get_index_from_id(agent_id)]
		self._agentlist.remove(agent)
		self._size -= 1
		self._topology.rm_agent(agent,pop=self)

	def pick_speaker(self):
 		return self.agent_pick.pick_speaker(self).get_id()

	def pick_hearer(self, speaker_id):
		speaker = self._agentlist[self.get_index_from_id(speaker_id)]
		return self.agent_pick.pick_hearer(speaker,self).get_id()

	def play_game(self, steps, **kwargs):
		for i in range(0,steps):
			self._evolution.step(pop=self)
			speaker = self.agent_pick.pick_speaker(pop=self)
			speaker_id = speaker.get_id()
			hearer = self.agent_pick.pick_hearer(speaker,pop=self)
			hearer_id = hearer.get_id()
			self._interaction.interact(speaker=speaker, hearer=hearer, pop=self)
#			tempmw=speaker.pick_mw()
#			ms=tempmw[0]
#			w=tempmw[1]
#			mh=hearer.guess_m(w)
#			if ms==mh:
#				speaker.success+=1
#				hearer.success+=1
#			else:
#				speaker.fail+=1
#				hearer.fail+=1
#			speaker.update_speaker(ms,w,mh)
#			hearer.update_hearer(ms,w,mh)
			self._lastgameinfo = self._interaction._last_info
			self._past = self._past[-99:]+[copy.deepcopy(self._lastgameinfo)]

	def get_lastgameinfo(self):
		return self._lastgameinfo

#	def reconstruct_from_info(self,game_info):
#		ms=game_info[0]
#		w=game_info[1]
#		mh=game_info[2]
#		sp_id=game_info[3]
#		hr_id=game_info[4]
#		speaker=self._agentlist[self.get_index_from_id(sp_id)]
#		hearer=self._agentlist[self.get_index_from_id(hr_id)]
#		if ms==mh:
#			speaker.success+=1
#			hearer.success+=1
#		else:
#			speaker.fail+=1
#			hearer.fail+=1
#		speaker.update_speaker(ms,w,mh)
#		hearer.update_hearer(ms,w,mh)
#		self._lastgameinfo = self._interaction


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



