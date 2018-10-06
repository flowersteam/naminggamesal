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

class StratDecisionVectorSoftmax(StratDecisionVector):
	def __init__(self, vu_cfg, **strat_cfg2):
		self.Temp = strat_cfg2['Temp']
		if 'N' in strat_cfg2.keys():
			self.N = strat_cfg2['N']
		StratDecisionVector.__init__(self,vu_cfg=vu_cfg, **strat_cfg2)


class StratDecisionVectorGainSoftmax(StratDecisionVectorSoftmax):

	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvec4_softmax_from_MW(M, W, self.Temp)
##############################

class StratDecisionVectorGainSoftmaxHearer(StratDecisionVectorSoftmax):

	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvec5_softmax_from_MW(M, W, self.Temp)
##############################

class StratDecisionVectorGainSoftmaxHearerTest(StratDecisionVectorSoftmax):
	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvectest_softmax_from_MW(M, W, self.Temp)
##############################

class StratDecisionVectorChunks(StratDecisionVectorSoftmax):
	def init_vector(self, voc):
		M = voc.get_M()
		W = voc.get_W()
		self.decision_vector = decvec_utils.decvec_chunks_from_MW(M=M, W=W, Temp=self.Temp, N=self.N)
##############################
