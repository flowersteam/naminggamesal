#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
evolution_class={
	'idle':'',
	'replace':'replace.Replace',
}

def get_evolution(evolution_type='idle', **evolution_cfg2):
	if evolution_type == 'idle':
		return Evolution
	else:	
		tempevo = evolution_type
		if tempevo in evolution_class.keys():
			tempevo = evolution_class[tempevo]
		templist = tempevo.split('.')
		temppath = '.'.join(templist[:-1])
		tempclass = templist[-1]
		_tempmod = import_module('.'+temppath,package=__name__)
		tempevo = getattr(_tempmod,tempclass)(**evolution_cfg2)
		return tempevo


class Evolution(object):

	def __init__(self, **evolution_cfg2):
		self._last_info = None
		for key, value in evolution_cfg2.iteritems():
			setattr(self, key, value)

	def get_evolutiontype(self):
		return self._evolutiontype

	def step(self, pop):
		pass
