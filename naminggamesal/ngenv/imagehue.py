from . import Environment
from scipy import misc
import colorsys
import random

class ImageHueEnv(Environment):
	_envs = {}
	def __init__(self, uuid_instance, files=[]):
		self.elements = []
		if uuid_instance in list(self._envs.keys()):
			self.__dict__ = self._envs[uuid_instance]
		else:
			self.uuid = uuid_instance
			if not isinstance(files,list):
				files = [files]
			for filename in files:
				image = misc.imread(filename)

				#self.elements = self.image.reshape((-1,self.image.shape[-1]))

				for x in range(image.shape[0]):
					for y in range(image.shape[1]):
						pixel = image[x,y,:].reshape(-1)
						pixel = pixel / 255.
						pixel_hsv = colorsys.rgb_to_hsv(*pixel)
						self.elements.append(pixel_hsv[0])
		self.reduce_elements()
		self._envs[uuid_instance] = self.__dict__

	def reduce_elements(self,nb=500):
		if len(self.elements) < nb:
			return None
		else:
			nb_el = len(self.elements)
			step = nb_el / float(nb-1)
			self.elements.sort()
			self.elements = [self.elements[int(i*step)] for i in range(nb)]


class HueDistribEnv(Environment):

	def __init__(self, uuid_instance, distrib='uniform'):
		self.uuid = uuid_instance
		self.distrib = distrib

	def get_element(self):
		if self.distrib == 'uniform':
			return random.random()
		else:
			return self.distrib(random.random())



