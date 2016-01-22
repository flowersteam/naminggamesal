#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class Omniscient(Interaction):
	def interact(self, speaker, hearer, pop, env):

		matrix_pop = pop.get_content()
		matrix_hearer = hearer.get_vocabulary_content()
		speaker._memory.update({'pop':matrix_pop,'hearer':matrix_hearer})
		ms ,w = speaker.pick_mw()
		if hearer._vocabulary.get_known_words(ms) == []:
			mh = ms
		else:
			mh = hearer.guess_m(w)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh)
		speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
		hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
		self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id]
