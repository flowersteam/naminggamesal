#!/usr/bin/python
import random
import numpy as np
from importlib import import_module


#####Classe de base
env_class={
	'image_hue':'imagehue.ImageHueEnv',
	'hue_distrib':'imagehue.HueDistribEnv',
	'graphenv':'graphenv.GraphEnv',
	'simple':'simple.SimpleEnv',
}



#class Singleton(type):
#	_instances = {}
#	def __call__(cls, uuid_instance, *args, **kwargs):
#		if (cls,uuid_instance) not in cls._instances:
#			cls._instances[(cls,uuid_instance)] = super(Singleton, cls).__call__(uuid_instance=uuid_instance, *args, **kwargs)
#		return cls._instances[cls,uuid_instance]
#	def __copy__(cls, instance):
#		return instance


class Environment(object):
	#__metaclass__ = Singleton
	def __init__(self, uuid_instance, **env_cfg2):
		self.uuid = uuid_instance
		for key, value in env_cfg2.iteritems():
			setattr(self, key, value)

	def get_envtype(self):
		return self._envtype

	def get_element(self):
		return random.choice(self.elements)

	def update_agent(self,agent,ms,w,mh=None,context=[]):
		pass

	def init_agent(self,agent):
		pass

	def get_M(self):
		return 0

	def get_W(self):
		return 0




def get_environment(env_type=None, **env_cfg2):
	if env_type is None:
		return Environment()
	tempenv = env_type
	if tempenv in env_class.keys():
		tempenv = env_class[tempenv]
	templist = tempenv.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempenv = getattr(_tempmod,tempclass)(**env_cfg2)
	return tempenv
