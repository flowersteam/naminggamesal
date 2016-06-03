#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
topology_class={
	'full_graph':'full_graph.FullGraph',
	'line':'line.Line',
	'circle':'line.Circle',
}

def get_topology(topology_type='full_graph', **topology_cfg2):
	temptp = topology_type
	if temptp in topology_class.keys():
		temptp = topology_class[temptp]
	templist = temptp.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	temptp = getattr(_tempmod,tempclass)(**topology_cfg2)
	return temptp


class Topology(object):

	def __init__(self, **topology_cfg2):
		self._last_info = None
		for key, value in topology_cfg2.iteritems():
			setattr(self, key, value)

	def get_topologytype(self):
		return self._topologytype

	def get_neighbor(self, speaker, pop):
		pass

	def add_agent(self, agent, pop):
		pass

	def rm_agent(self, agent, pop):
		pass
