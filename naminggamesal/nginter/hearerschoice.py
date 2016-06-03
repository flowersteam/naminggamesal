#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class HearersChoice(Interaction):
	def interact(self, speaker, hearer, pop):
		ms = hearer.hearer_pick_m()
		w =  speaker.pick_w(ms)
		mh = hearer.guess_m(w)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh)
		speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
		hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
		self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id]
