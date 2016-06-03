#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
agentpick_class={
	'random_pick':'random_pick.RandomPick',
	'neighbor_pick':'neighbor_pick.NeighborPick',
}

def get_agentpick(agentpick_type='random_pick', **agentpick_cfg2):
	tempap = agentpick_type
	if tempap in agentpick_class.keys():
		tempap = agentpick_class[tempap]
	templist = tempap.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempap = getattr(_tempmod,tempclass)(**agentpick_cfg2)
	return tempap


class AgentPick(object):

	def __init__(self, **agentpick_cfg2):
		self._last_info = None
		for key, value in agentpick_cfg2.iteritems():
			setattr(self, key, value)

	def get_agentpicktype(self):
		return self._agentpicktype

	def agentpick(self, speaker, hearer, pop):
		pass
