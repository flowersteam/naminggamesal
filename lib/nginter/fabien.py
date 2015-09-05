#!/usr/bin/python

from . import BaseInteraction
import random
import numpy as np
from .. import ngmeth


def proba_info(agent1, agent2):        #based on information measure
	tempmat = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
	tempm = np.sum(tempmat)
	return ngmeth.tempentropy(agent1._M-tempm, agent2._W-tempm)


def FUNC2(agent1, agent2):         #always half
	return 0.5

def FUNC3(agent1, agent2):         #random (equivalent to 0.5?)
	return random.random()


##########
class FabienInteraction(BaseInteraction):

	def __init__(self, proba_func='proba_info', **interact_cfg2):
		super(FabienInteraction,self).__init__(self, **interact_cfg2)
		self.proba_func = locals()[proba_func]  #Use globals or locals?


	def interact(self, speaker, hearer):
		r = random.random()
		if self.proba_func(speaker, hearer) > r:
			self.base_interact(speaker, hearer)

	def base_interact(self, speaker, hearer):
		ms = speaker.pick_m()
		w =  speaker.pick_w(ms)
		mh = hearer.guess_m(w)
		if ms == mh:
			speaker.success += 1
			hearer.success += 1
		else:
			speaker.fail += 1
			hearer.fail += 1
		speaker.update_speaker(ms, w, mh)
		hearer.update_hearer(ms, w, mh)
		self._last_info = [ms, w, mh, speaker._id, hearer._id]
