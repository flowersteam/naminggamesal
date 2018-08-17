
from .naive import StratNaive
import random
import numpy as np



##################################### COHERENCE STRATEGY ########################################
class StratCoherence(StratNaive):

	def __init__(self, vu_cfg, time_scale=5 , threshold=1.-10**(-5),**strat_cfg2):
		StratNaive.__init__(self,vu_cfg=vu_cfg, **strat_cfg2)
		self.time_scale = time_scale
		self.threshold = threshold
		#mp = {'mem_type':'past_interactions_sliding_window_local'}
		#if mp not in self.memory_policies:
		#	self.memory_policies.append(mp)


	def hearer_pick_m(self,voc,mem, context):
		return self.pick_m(voc, mem, context)

	def get_counts(self, voc, mem):
		countlist = {}
		for m in voc.get_known_meanings():
			if m in list(mem['past_interactions_sliding_window_local'].keys()):
				w_l = mem['past_interactions_sliding_window_local']['m'][m]
				countlist[m] = max([len([w1 for w1 in w_l if w1==w]) for w in w_l])
		return countlist

	def pick_m(self, voc, mem, context):
		counts = self.get_counts(voc, mem)
		if not len(counts.values()) or min(list(counts.values()))>=self.threshold*self.time_scale:
			return voc.get_new_unknown_m()
		else:
			KM = voc.get_known_meanings()
			val = max([v for v in list(counts.values()) if v < self.threshold*self.time_scale])
			tempm = [m for m in KM if counts[m] == val]
			return random.choice(tempm)


class StratCoherenceLast(StratCoherence):

	def get_counts(self, voc, mem):
		countlist = {}
		for m in voc.get_known_meanings():
			if m in list(mem['past_interactions_sliding_window_local'].keys()):
				w_l = mem['past_interactions_sliding_window_local']['m'][m]
				countlist[m] = len([w1 for w1 in w_l if w1==w_l[-1]])
		return countlist
