#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class Omniscient(Interaction):
	def interact(self, speaker, hearer, pop,simulated=False):

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
			pop.env.update_agent(speaker,ms=ms,w=w,mh=mh)
			pop.env.update_agent(hearer,ms=ms,w=w,mh=mh)
			speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
			self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]
		else:
			return [ms,w,mh,bool_succ,speaker._id,hearer._id,bool_newconv]
