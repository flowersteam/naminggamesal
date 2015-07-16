#!/usr/bin/python
# -*- coding: latin-1 -*-

from .naive import StratNaive
from .naive import StratNaiveReal
import random
import numpy as np
from .. import ngmeth


################################### STRATEGIE DECISION VECTOR #########################################""

#Ne pas oublier STRATTYPE, NAME et l'initialisation dans la classe strategy

class StratDecisionVector(StratNaive):

	def pick_mw(self,voc,mem):
		Mtemp=len(voc.get_known_meanings())
		tirage=random.random()
		if tirage<self.decision_vector[Mtemp]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		w=self.pick_w(m,voc,mem)
		return([m,w])


	def init_memory(self,voc):
		return {}
################################### STRATEGIE DECISION VECTOR REELLE#########################################""


class StratDecisionVectorReal(StratNaiveReal):

	def pick_mw(self,voc,mem):
		Mtemp=len(voc.get_known_meanings())
		tirage=random.random()
		if tirage<self.decision_vector[Mtemp]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		w=self.pick_w(m,voc,mem)
		return([m,w])


	def init_memory(self,voc):
		return {}


################################### STRATEGIE DECISION VECTOR GAIN MAXIMIZATION #########################################""


class StratDecisionVectorGainmax(StratDecisionVector):
	def __init__(self, **strat_cfg2):
		M = strat_cfg2['M']
		W = strat_cfg2['W']
		self.decision_vector = ngmeth.decvec3_from_MW(M, W)
##############################
