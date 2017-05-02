#!/usr/bin/python

from . import Interaction
import random
import numpy as np

##########
class CategoryGameSpeakersChoice(Interaction):
	def interact(self, speaker, hearer, pop,simulated=False):
		ct = speaker.pick_context(env=pop.env, size=2)
		ms = speaker.pick_m(context=ct)
		w = speaker.pick_w(ms)
		mh = hearer.guess_m(w,ct)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh, context=ct)
		if not simulated:
			speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ,context=ct)
			hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ,context=ct)
			self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id,ct]
		else:
			return [ms,w,mh,bool_succ,speaker._id,hearer._id,ct]

##########
class CategoryGameHearersChoice(Interaction):
	def interact(self, speaker, hearer, pop,simulated=False):
		ct = hearer.pick_context(env=pop.env, size=2)
		ms = speaker.pick_m(context=ct)
		w = speaker.pick_w(ms)
		mh = hearer.guess_m(w,ct)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh, context=ct)
		if not simulated:
			speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ,context=ct)
			hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ,context=ct)
			self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id,ct]
		else:
			return [ms,w,mh,bool_succ,speaker._id,hearer._id,ct]
