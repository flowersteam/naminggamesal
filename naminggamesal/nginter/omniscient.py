#!/usr/bin/python

from . import Interaction,get_interaction
from ..ngagent.ngmem import get_memory
import random
import copy
import numpy as np

##########
class OmniscientOld(Interaction):
	def interact(self, speaker, hearer, pop, current_game_info,simulated=False):
		if not simulated:
			speaker.warn(role='speaker')
			hearer.warn(role='hearer')
		matrix_pop = pop.get_content()
		#matrix_hearer = hearer.get_vocabulary_content()
		#speaker._memory.update({'pop':matrix_pop,'hearer':matrix_hearer})
		speaker._memory.update({'success_mw':matrix_pop,'failure_mw':np.zeros(matrix_pop.shape)})
		hearer._memory.update({'success_mw':matrix_pop,'failure_mw':np.zeros(matrix_pop.shape)})
		ms = speaker.pick_m()
		w = speaker.pick_w(m=ms)
		#ms ,w = speaker.pick_mw()
		#if hearer._vocabulary.get_known_words(ms) == []:
		#	mh = ms
		#else:
		mh = hearer.guess_m(w)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh)
		bool_newconv = (ms not in speaker._vocabulary.get_known_meanings())
		if not simulated:
			pop.env.update_agent(speaker,ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			pop.env.update_agent(hearer,ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]
		else:
			return [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]

class Omniscient(Interaction):
	def __init__(self,subinteract_cfg,**interact_cfg_2):
		self.subinteract = get_interaction(**subinteract_cfg)
		#self.memory_policies = memory_policies
		#self._memory = get_memory(self.memory_policies)
		Interaction.__init__(self,**interact_cfg_2)

	def interact(self, speaker, hearer, pop, current_game_info,simulated=False):
		#for v in list(self._memory.values()):
		#	if hasattr(v,'rebuild_global_mem'):
		#		v.rebuild_global_mem(pop)
		
		v = pop._agentlist[0]._vocabulary.__class__(start='empty',normalized=False)
		v.discover_meanings(pop._agentlist[0]._vocabulary.get_accessible_meanings())
		v.discover_words(pop._agentlist[0]._vocabulary.get_accessible_words())
		for ag in pop._agentlist:
			v = v + ag._vocabulary #implement auto discover meanings
		v = v/len(pop._agentlist)
		v.is_normalized = True
		speaker._memory['interact_count_voc'] = copy.deepcopy(v)
		hearer._memory['interact_count_voc'] = copy.deepcopy(v)
		#speaker._memory.update(copy.deepcopy(self._memory))
		#hearer._memory.update(copy.deepcopy(self._memory))
		#self._memory.clean()
		return self.subinteract.interact(speaker=speaker, hearer=hearer, pop=pop, current_game_info=current_game_info,simulated=simulated)