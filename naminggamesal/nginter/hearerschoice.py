#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class HearersChoice(Interaction):
	def interact(self, speaker, hearer, pop, current_game_info,simulated=False,optimized=True):
		if not simulated:
			speaker.warn(role='speaker')
			hearer.warn(role='hearer')
		ms = hearer.hearer_pick_m()
		w =  speaker.pick_w(ms)
		mh = hearer.guess_m(w)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh)
		bool_newconv = (mh not in hearer._vocabulary.get_known_meanings())
		if not simulated:
			pop.env.update_agent(speaker,ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			pop.env.update_agent(hearer,ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]
		else:
			return [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]


class HearersChoiceEpirob(Interaction):
	def interact(self, speaker, hearer, pop, current_game_info,simulated=False,optimized=True):
		if not simulated:
			speaker.warn(role='speaker')
			hearer.warn(role='hearer')
		ms = hearer.hearer_pick_m()
		w = speaker.pick_w(ms)
		if hearer._vocabulary.get_known_meanings(w):
			mh = hearer.guess_m(w)
		else:
			mh = ms
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh)
		bool_newconv = (mh not in hearer._vocabulary.get_known_meanings())
		if not simulated:
			if speaker._vocabulary.get_known_meanings() or random.random()<0.001:
				pop.env.update_agent(speaker,ms=ms,w=w,mh=mh,bool_succ=bool_succ)
				pop.env.update_agent(hearer,ms=ms,w=w,mh=mh,bool_succ=bool_succ)
				speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
				hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]
		else:
			return [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]

