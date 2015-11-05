#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class Omniscient(Interaction):
	def interact(self, speaker, hearer, pop):

		matrix_pop = pop.get_content()
		matrix_hearer = hearer.get_vocabulary_content()
		speaker._memory.update({'pop':matrix_pop,'hearer':matrix_hearer})
		ms ,w = speaker.pick_mw()
		if hearer._vocabulary.get_known_words(ms) == []:
			mh = ms
		else:
			mh = hearer.guess_m(w)
		if ms == mh:
			speaker.success += 1
			hearer.success += 1
		else:
			speaker.fail += 1
			hearer.fail += 1
		speaker.update_speaker(ms,w,mh)
		hearer.update_hearer(ms,w,mh)
		self._last_info = [ms,w,mh,speaker._id,hearer._id]
