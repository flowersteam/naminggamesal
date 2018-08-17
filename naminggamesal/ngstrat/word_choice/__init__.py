#!/usr/bin/python
import random
import numpy as np
from importlib import import_module
import copy


wordchoice_class = {
	'random':'randomchoice.RandomWordChoice',

	'membased':'membased.MemBasedWordChoice',

	'word_preference':'word_preference.WordPreference',
	'play_smart':'word_preference.PlaySmart',
	'play_last':'word_preference.PlayLast',
	'play_first':'word_preference.PlayFirst',
}

def get_wordchoice(wordchoice_type='random', **wordchoice_cfg2):
	tempstr = wordchoice_type
	if tempstr in list(wordchoice_class.keys()):
		tempstr = wordchoice_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	wordchoice = getattr(_tempmod,tempclass)(**wordchoice_cfg2)
	wordchoice._wordchoicetype = wordchoice_type
	return wordchoice


class BaseWordChoice(object):
	def __init__(self,memory_policies=[],mem_policy=None):
		self.memory_policies = copy.deepcopy(memory_policies)
		if mem_policy is not None:
			self.memory_policies.append(mem_policy)

	def get_wordchoicetype(self):
		return self._wordchoicetype

	def pick_w(self,m,voc,mem,context=[]):
		pass
