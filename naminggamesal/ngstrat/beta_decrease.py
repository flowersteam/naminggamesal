
from .naive import StratNaive
import random
import numpy as np

class BetaDecreaseStrat(StratNaive):
	def __init__(self, vu_cfg, time_scale=0.9, **strat_cfg2):
		StratNaive.__init__(self,vu_cfg=vu_cfg, **strat_cfg2)
		self.time_scale = time_scale

	def update_speaker(self, ms, w, mh, voc, mem, bool_succ, context=[]):
		self.voc_update.beta = max(0,self.voc_update.beta - 1./self.time_scale)
		return self.voc_update.update_speaker(ms, w, mh, voc, mem, bool_succ, context)

	def update_hearer(self, ms, w, mh, voc, mem, bool_succ, context=[]):
		self.voc_update.beta = max(0,self.voc_update.beta - 1./self.time_scale)
		return self.voc_update.update_hearer(ms, w, mh, voc, mem, bool_succ, context)
