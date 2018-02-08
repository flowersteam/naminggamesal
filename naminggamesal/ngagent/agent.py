#!/usr/bin/python

#import random
#from ngvoc import *
import os
from copy import deepcopy
import pickle
import random
import matplotlib.pyplot as plt
import uuid

from .. import ngvoc
from .. import ngstrat
from . import ngsensor
from . import ngmem

class Agent(object):
	def __init__(self, voc_cfg, strat_cfg, sensor_cfg=None, memory_policies=[], agent_id=None, env=None):
		self.cfg = {'voc_cfg':deepcopy(voc_cfg),'strat_cfg':deepcopy(strat_cfg),'sensor_cfg':deepcopy(sensor_cfg)}
		if agent_id is None:
			self._id = str(uuid.uuid1())
		else:
			self._id = agent_id;
		self._vocabulary = ngvoc.get_vocabulary(env=env,**voc_cfg)
		self._strategy = ngstrat.get_strategy(**strat_cfg)
		self.memory_policies = deepcopy(memory_policies)
		if hasattr(self._strategy,'memory_policies'):
			for mp in self._strategy.memory_policies:
				if not [mmp for mmp in self.memory_policies if mmp == mp]:
					self.memory_policies.append(mp)
		if sensor_cfg is not None:
			self._sensoryapparatus = ngsensor.get_sensor(**sensor_cfg)

		if hasattr(self._vocabulary,'_M'):
			self._M = self._vocabulary._M
			self._W = self._vocabulary._W
		self.init_memory()
		self.fail = 0
		self.success = 0

	def init_memory(self):
		self._memory = ngmem.get_memory(memory_policies=self.memory_policies,voc=self._vocabulary,cfg=deepcopy(self.cfg))#self._strategy.init_memory(self._vocabulary)

	def get_vocabulary_content(self):
		return self._vocabulary.get_content()

	def get_voctype(self):
		return self._vocabulary.get_voctype()

	def get_id(self):
		return self._id

#	def __str__(self):
#		return str(self._vocabulary)

	def pick_m(self,context=[]):
		return self._strategy.pick_m(self._vocabulary,self._memory,context=context)

	def pick_mw(self,context=[]):
		return self._strategy.pick_mw(self._vocabulary,self._memory,context=context)

	def hearer_pick_m(self,context=[]):
		try:
			return self._strategy.hearer_pick_m(self._vocabulary,self._memory,context=context)
		except:
			print(self._strategy)
			raise

	def pick_new_m(self):
		return self._strategy.pick_new_m(self._vocabulary,self._memory)

	def guess_m(self,w, context=[]):
		if w not in self._vocabulary.get_accessible_words():
			self.discover_words([w])
		return self._strategy.guess_m(w,self._vocabulary,self._memory, context=context)

	def pick_w(self,m, context=[]):
		return self._strategy.pick_w(m,self._vocabulary,self._memory,context)

	def update_hearer(self,ms,w,mh,bool_succ,context=[]):
		self._strategy.update_hearer(ms=ms,w=w,mh=mh,voc=self._vocabulary,mem=self._memory,bool_succ=bool_succ,context=context)
		#self._strategy.update_memory(ms,w,mh,self._vocabulary,self._memory,role='hearer', bool_succ=bool_succ,context=context)
		self._memory.update_memory(ms,w,mh,self._vocabulary,role='hearer', bool_succ=bool_succ,context=context)
		if bool_succ:
			self.success += 1
		else:
			self.fail += 1


	def update_speaker(self,ms,w,mh,bool_succ,context=[]):
		self._strategy.update_speaker(ms=ms,w=w,mh=mh,voc=self._vocabulary,mem=self._memory,bool_succ=bool_succ,context=context)
		#self._strategy.update_memory(ms,w,mh,self._vocabulary,self._memory,role='speaker', bool_succ=bool_succ,context=context)
		self._memory.update_memory(ms,w,mh,self._vocabulary,role='speaker', bool_succ=bool_succ,context=context)
		if bool_succ:
			self.success += 1
		else:
			self.fail += 1


	def visual(self,vtype=None,iterr=100,mlist="all",wlist="all"):
		self._strategy.visual(self._vocabulary,mem=self._memory,vtype=vtype,iterr=iterr,mlist=mlist,wlist=wlist)

	def eval_success(self, ms, w, mh,context=[]):
		return self._strategy.success.eval(ms=ms, w=w, mh=mh, voc=self._vocabulary, mem=self._memory, strategy=self._strategy,context=context)

	def pick_context(self, env, size=2, diff=True):
		return self._strategy.pick_context(voc=self._vocabulary,mem=self._memory,context_gen=self._sensoryapparatus.context_gen(env=env, diff=diff, size=size))


	def warn(self,role):
		pass

	def perceive(self,input_signal,env=None):
		self._sensoryapparatus.perceive(input_signal=input_signal,env=env)

	def discover_meanings(self,m_list):
		for mem_key in list(self._memory.keys()):
			if hasattr(self._memory[mem_key],'discover_meanings'):
				self._memory[mem_key].discover_meanings(m_list=m_list)
		return self._vocabulary.discover_meanings(m_list)

	def discover_words(self,w_list):
		for mem_key in list(self._memory.keys()):
			if hasattr(self._memory[mem_key],'discover_words'):
				self._memory[mem_key].discover_words(w_list=w_list)
		return self._vocabulary.discover_words(w_list)