#!/usr/bin/python
import random
import numpy as np
from importlib import import_module

#####Classe de base
sensor_class={
'human_hue':'humanhue.HumanHueSA',
'uniform_hue':'uniformhue.UniformHueSA',
}

def get_sensor(sensor_type='perfect', **sensor_cfg2):
	tempstr = sensor_type
	if tempstr in list(sensor_class.keys()):
		tempstr = sensor_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	return getattr(_tempmod,tempclass)(**sensor_cfg2)

class SensoryApparatus(object):
	def __init__(self):
		pass

	def perceive(self, input_signal, env=None):
		return input_signal

	def discriminable(self, input_sig1, input_sig2):
		if input_sig1 != input_sig2:
			return True
		else:
			return False

	def pick_context(self, size=2, diff=True, tries=100, env=None):
		if not diff:
			return [env.get_element() for i in range(size)]
		else:
			context = []
			for s in range(size):
				s1 = env.get_element()
				for s2 in range(s):
					if not self.discriminable(s1, context[s2]):
						if tries == 0:
							raise Exception('Could not find enough discriminable elements in environment')
						else:
							return self.pick_context(size=size,diff=diff,tries=tries-1,env=env)
				context.append(s1)
			return context

	def context_gen(self, size=2, diff=True, tries=100, env=None):
		while True:
			yield self.pick_context(size=size, diff=diff, tries=tries, env=env)


