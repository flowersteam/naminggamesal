#!/usr/bin/python
# -*- coding: latin-1 -*-

from .naive import StratNaive
from .naive import StratNaiveReal
import random
import numpy as np


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

#Ne pas oublier STRATTYPE, NAME et l'initialisation dans la classe strategy

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



