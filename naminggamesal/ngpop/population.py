#!/usr/bin/python

#import random
#from ngvoc import *
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import uuid
import copy
import json

from ..ngagent import get_agent
from ..nginter import get_interaction
from ..ngtopology import get_topology
from ..ngenv import get_environment
from ..ngagentpicking import get_agentpick
from ..ngagentinit import get_agent_init
from ..ngevol import get_evolution

import networkx as nx


class Population(object):

	def __init__(self, voc_cfg, strat_cfg, interact_cfg, nbagent, agent_init_cfg={'agent_init_type':'agent_init'}, evolution_cfg={'evolution_type':'idle'}, agentpick_cfg={'agentpick_type':'random_pick'}, sensor_cfg=None, env_cfg=None,topology_cfg={'topology_type':'full_graph'},xp_uuid=None):
		self._size = 0
		self._strat_cfg = strat_cfg
		self._agent_init_cfg = agent_init_cfg
		self.agent_init = get_agent_init(**agent_init_cfg)
		self._agentpick_cfg = agentpick_cfg
		self.agent_pick = get_agentpick(**agentpick_cfg)
		self._sensor_cfg = sensor_cfg
		self._env_cfg = env_cfg
		self._interaction = get_interaction(**interact_cfg)
		self._evolution = get_evolution(**evolution_cfg)
		self._exec_time = 0.
		self.xp_uuid = xp_uuid
		self.uuid = str(uuid.uuid1())
		if env_cfg is None:
			self.env = None
		else:
			if 'uuid_instance' not in list(self._env_cfg.keys()):
				self.env_id = str(uuid.uuid1())
			else:
				self.env_id = self._env_cfg['uuid_instance']
			self.env = get_environment(uuid_instance=self.env_id,**self._env_cfg)
		self._voc_cfg = voc_cfg
		if 'M' in list(voc_cfg.keys()):
			self._M = voc_cfg['M']
			self._W = voc_cfg['W']
		elif 'subvoc_cfg' in list(voc_cfg.keys()) and 'M' in list(voc_cfg['subvoc_cfg'].keys()):
			self._M = voc_cfg['subvoc_cfg']['M']
			self._W = voc_cfg['subvoc_cfg']['W']
		self._lastgameinfo = []
		self._past = []
		self._agentlist = []
		for i in range(nbagent):
			self.add_new_agent(agent_id=None, strat_cfg=strat_cfg, voc_cfg=voc_cfg, sensor_cfg=sensor_cfg, pop_init=True)
		self._topology = get_topology(pop=self,**topology_cfg)


	def get_size(self):
		return self._size

	def get_M(self):
		if hasattr(self,'_M'):
			return self._M
		else:
			return self.env.get_M()

	def get_W(self):
		if hasattr(self,'_W'):
			return self._W
		else:
			return self.env.get_W()

	#def get_vocsize(self):
	#	return [self._M,self._W]

	def check_id(self,agent_id):
		for i in range(0,len(self._agentlist)):
			if self._agentlist[i].get_id() == agent_id:
				return 1
		return 0

	def add_agent(self, agent):
		if self.check_id(agent.get_id()) == 1:
			print("WARNING: 2 agents with same identity")
		self._agentlist.append(agent)
		self._size+=1
		if hasattr(self,'_topology'):
			self._topology.add_agent(agent,pop=self)

	def idmax(self): #Suppose ID=nombre
		tempid=0
		for i in range(0,len(self._agentlist)):
			tempid=max(tempid,self._agentlist[i].get_id())
		return tempid

	def add_new_agent(self, voc_cfg=None, strat_cfg=None, sensor_cfg=None, agent_id=None, pop_init=False):
		if voc_cfg is None:
			voc_cfg = self._voc_cfg
		if strat_cfg is None:
			strat_cfg = self._strat_cfg
		if sensor_cfg is None:
			sensor_cfg = self._sensor_cfg
		new_cfg = self.agent_init.modify_cfg(voc_cfg=voc_cfg, strat_cfg=strat_cfg, sensor_cfg=sensor_cfg, agent_id=agent_id, env=self.env,pop_init=pop_init)
		agent = get_agent(**new_cfg)
		self.agent_init.modify_agent(agent,pop=self,pop_init=pop_init)
		self.add_agent(agent)

	def get_index_from_id(self, agent_id):
		for i in range (0,len(self._agentlist)):
			if self._agentlist[i].get_id() == agent_id:
				return i
		print("id does not exist")

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
		#if not hasattr(self,'current_game_info'):

		filename = self.get_current_info_filename()
		if os.path.isfile(filename):
			with open(filename,'r') as f:
				self.current_game_info = json.loads(f.read())
			os.remove(filename)
		else:
			self.current_game_info = {}
		try:
			for i in range(0,steps):
				self._evolution.step(pop=self)
				if 'speaker_id' not in list(self.current_game_info.keys()):
					speaker = self.agent_pick.pick_speaker(pop=self)
					speaker_id = speaker.get_id()
					self.current_game_info['speaker_id'] = speaker_id
				else:
					speaker_id = self.current_game_info['speaker_id']
					speaker = self._agentlist[self.get_index_from_id(speaker_id)]

				if 'hearer_id' not in list(self.current_game_info.keys()):
					hearer = self.agent_pick.pick_hearer(speaker,pop=self)
					hearer_id = hearer.get_id()
					self.current_game_info['hearer_id'] = hearer_id
				else:
					hearer_id = self.current_game_info['hearer_id']
					hearer = self._agentlist[self.get_index_from_id(hearer_id)]
				self._interaction.interact(speaker=speaker, hearer=hearer, pop=self, current_game_info=self.current_game_info)
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
				self.current_game_info = {}
		except IOError as e:
			if str(e) == 'User intervention needed':
				if not os.path.isdir(os.path.dirname(filename)):
					os.makedirs(os.path.dirname(filename))
				with open(filename,'w') as f:
					f.write(json.dumps(self.current_game_info))
			raise

	def get_current_info_filename(self):
		if hasattr(self,'xp_uuid') and self.xp_uuid is not None:
			uuid_str = self.xp_uuid
		else:
			uuid_str = self.uuid
		return './data/current_game_info/'+ uuid_str + '.txt'

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
			temprep=np.matrix(np.zeros((self.get_M(),self.get_W())))
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
			ag_list=list(range(0,len(self._agentlist)))
		if vtype==None:
			tempstr += "nbagent: "+str(self._size)+"\n"
			temprep=np.matrix(np.zeros((self.get_M(),self.get_W())))
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
				print(("Agent ID: "+str(self._agentlist[i].get_id())+"\n"))
				self._agentlist[i].visual(vtype=vtype)
				print("\n")

	def get_content(self,*args):
		if len(args)==0:
			temprep=np.matrix(np.zeros((self.get_M(),self.get_W())))
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
			print("Agent ID: %s" %args)
			print(str(self._agentlist[i]))


	def draw(self, draw_type=None, fig=None,write=True):
		if fig is None:
			fig = plt.figure()

		plt.figure(fig.number)

		def color_of_node(m):
			nag = 0
			for ag in self._agentlist:
				if m in ag._vocabulary.get_known_meanings():
					nag += 1
				ag._vocabulary.del_cache()
			val = nag/float(len(self._agentlist))
			if val == 0:
				return (1,0,0)
			elif val == 1.:
				return (0,1,0)
			else:
				return (1-val,1-val,1)
			#return (random.random(),random.random(),random.random())


		G = self.env.meaning_graph
		pos = self.env.meaning_graph_pos#nx.spring_layout(G)
		node_list = G.nodes()
		node_color = []
		labels = {}
		for m in node_list:
			labels[m] = str(m)
			col = color_of_node(m)
			node_color.append(col)
			G.node[m]['viz'] = {'color':{'r':int(col[0]*255),'g':int(col[1]*255),'b':int(col[2]*255),'a':int(0.8*255)}}

		#plt.clf()
		#plt.ion()
		#plt.axes('off')
		art1 = nx.draw_networkx_edges(G,pos)#,width=1.0,alpha=0.5)
		art2 = nx.draw_networkx_nodes(G,pos,nodelist=node_list,node_color=node_color,alpha=0.8)

		if write:
			nx.write_gexf(G,'test.gexf')

		return G

