#!/usr/bin/python

from .naive import StratNaive
import random
import numpy as np
from ..ngmeth_utils import decvec_utils


################################### STRATEGIE DECISION VECTOR #########################################""

#Ne pas oublier STRATTYPE, NAME et l'initialisation dans la classe strategy

class StratDecisionVector(StratNaive):

	def __init__(self, vu_cfg, **strat_cfg2):
		super(StratDecisionVector, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)

	def pick_m(self,voc,mem):
		Mtemp=len(voc.get_known_meanings())
		tirage=random.random()
		if tirage<self.decision_vector[Mtemp]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		return m

################################### STRATEGIE DECISION VECTOR GAIN MAXIMIZATION #########################################""


class StratDecisionVectorGainmax(StratDecisionVector):
	def __init__(self, vu_cfg, **strat_cfg2):
		super(StratDecisionVectorGainmax, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		M = strat_cfg2['M']
		W = strat_cfg2['W']
		self.decision_vector = decvec_utils.decvec3_from_MW(M, W)
##############################


class StratDecisionVectorGainSoftmax(StratDecisionVector):
	def __init__(self, **strat_cfg2):
		super(StratDecisionVectorGainSoftmax, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		M = strat_cfg2['M']
		W = strat_cfg2['W']
		Temp = strat_cfg2['Temp']
		self.decision_vector = decvec_utils.decvec4_softmax_from_MW(M, W, Temp)
##############################

class StratDecisionVectorGainSoftmaxHearer(StratDecisionVector):
	def __init__(self, **strat_cfg2):
		super(StratDecisionVectorGainSoftmaxHearer, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		M = strat_cfg2['M']
		W = strat_cfg2['W']
		Temp = strat_cfg2['Temp']
		self.decision_vector = decvec_utils.decvec5_softmax_from_MW(M, W, Temp)
##############################

class StratDecisionVectorGainSoftmaxHearerTest(StratDecisionVector):
	def __init__(self, **strat_cfg2):
		super(StratDecisionVectorGainSoftmaxHearerTest, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		M = strat_cfg2['M']
		W = strat_cfg2['W']
		Temp = strat_cfg2['Temp']
		self.decision_vector = decvec_utils.decvectest_softmax_from_MW(M, W, Temp)
##############################
