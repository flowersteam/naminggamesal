#!/usr/bin/python
import random
import numpy as np
from importlib import import_module


#####Classe de base
env_class={
	'image_hue':'imagehue.ImageHueEnv',
}

def get_environment(env_type=None, **env_cfg2):
	if env_type is None:
		return None
	tempenv = env_type
	if tempenv in env_class.keys():
		tempenv = env_class[tempenv]
	templist = tempenv.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempenv = getattr(_tempmod,tempclass)(**env_cfg2)
	return tempenv


class Environment(object):

	def __init__(self, **env_cfg2):
		for key, value in env_cfg2.iteritems():
			setattr(self, key, value)

	def get_envtype(self):
		return self._envtype

	def get_element(self):
		return random.choice(self.elements)

