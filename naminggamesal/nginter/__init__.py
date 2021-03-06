#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####
interaction_class={
	'hearerschoice':'hearerschoice.HearersChoice',
	'speakerschoice':'speakerschoice.SpeakersChoice',
	'speakerschoiceomniscient':'speakerschoice.SpeakersChoiceOmniscient',
	'hearerschoice_epirob':'hearerschoice.HearersChoiceEpirob',
	'speakerschoice_epirob':'speakerschoice.SpeakersChoiceEpirob',
	'fabien':'fabien.FabienInteraction',
	'omniscient':'omniscient.Omniscient',
	'category_game':'category_game.CategoryGameSpeakersChoice',
	'category_game_speakerschoice':'category_game.CategoryGameSpeakersChoice',
	'category_game_hearerschoice':'category_game.CategoryGameHearersChoice',
	'meaning_exploration':'meaning_exploration.MeaningExploration',
}

def get_interaction(interact_type='speakerschoice', **interact_cfg2):
	tempint = interact_type
	if tempint in list(interaction_class.keys()):
		tempint = interaction_class[tempint]
	templist = tempint.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempinter = getattr(_tempmod,tempclass)(**interact_cfg2)
	return tempinter


class Interaction(object):

	def __init__(self, **interact_cfg2):
		self._last_info = None
		for key, value in interact_cfg2.items():
			setattr(self, key, value)

	def get_interacttype(self):
		return self._interacttype

	def interact(self, speaker, hearer, pop, current_game_info, simulated=False):
		pass
