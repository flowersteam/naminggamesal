#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class HearersChoice(Interaction):
	def interact(self, speaker, hearer, pop):
		ms = hearer.hearer_pick_m()
		w =  speaker.pick_w(ms)
		if hearer._vocabulary.get_known_words(ms) == []:
			mh = ms
		else:
			mh = hearer.guess_m(w)
		if ms==mh:
			speaker.success+=1
			hearer.success+=1
		else:
			speaker.fail+=1
			hearer.fail+=1
		speaker.update_speaker(ms,w,mh)
		hearer.update_hearer(ms,w,mh)
		self._last_info = [ms,w,mh,speaker._id,hearer._id]
