#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
interaction_class={
	'hearerschoice':'hearerschoice.HearersChoice',
	'speakerschoice':'speakerschoice.SpeakersChoice',
	'fabien':'fabien.FabienInteraction'
}

def Interaction(interact_type='speakerschoice', **interact_cfg2):
	tempint = interact_type
	if tempint in interaction_class.keys():
		tempint = interaction_class[tempint]
	templist = tempint.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempinter = getattr(_tempmod,tempclass)(**interact_cfg2)
	return tempinter


class BaseInteraction(object):

	def __init__(self, **interact_cfg2):
		self._last_info = None
		for key, value in interact_cfg2.iteritems():
			setattr(self, key, value)

	def get_interacttype(self):
		return self._interacttype
