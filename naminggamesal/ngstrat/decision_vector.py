#!/usr/bin/python

from .naive import StratNaive
import random
import numpy as np
from ..ngmeth_utils import decvec_utils


################################### DECISION VECTOR #########################################""



class StratDecisionVector(StratNaive):
	def __init__(self, vu_cfg, **strat_cfg2):
		super(StratDecisionVector, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		if 'decision_vector' in strat_cfg2.keys():
			self.decision_vector = strat_cfg2['decision_vector']

	def pick_m(self,voc,mem,context=[]):
		if not hasattr(self,'decision_vector'):
			self.init_vector(voc=voc)
		Mtemp = len(voc.get_known_meanings())
		tirage = random.random()
		if tirage < self.decision_vector[Mtemp]:
			return voc.get_new_unknown_m()
		else:
			return voc.get_random_known_m()

################################### DECISION VECTOR GAIN MAXIMIZATION #########################################""


class StratDecisionVectorGainmax(StratDecisionVector):
	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvec3_from_MW(M, W)
##############################


class StratDecisionVectorGainSoftmax(StratDecisionVector):
	def __init__(self, vu_cfg, **strat_cfg2):
		super(StratDecisionVectorGainSoftmax, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		self.Temp = strat_cfg2['Temp']

	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvec4_softmax_from_MW(M, W, self.Temp)
##############################

class StratDecisionVectorGainSoftmaxHearer(StratDecisionVector):
	def __init__(self, vu_cfg, **strat_cfg2):
		super(StratDecisionVectorGainSoftmax, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		self.Temp = strat_cfg2['Temp']

	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvec5_softmax_from_MW(M, W, self.Temp)
##############################

class StratDecisionVectorGainSoftmaxHearerTest(StratDecisionVector):
	def __init__(self, vu_cfg, **strat_cfg2):
		super(StratDecisionVectorGainSoftmax, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		self.Temp = strat_cfg2['Temp']

	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvectest_softmax_from_MW(M, W, self.Temp)
##############################
