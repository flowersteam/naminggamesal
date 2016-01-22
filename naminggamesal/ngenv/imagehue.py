from . import Environment
from scipy import misc
import colorsys

class ImageHueEnv(Environment):
	def __init__(self, files):
		if not isinstance(files,list):
			files = [files]
		for filename in files:
			self.image = misc.imread(filename)

		#self.elements = self.image.reshape((-1,self.image.shape[-1]))
		self.elements = []
		for x in range(self.image.shape[0]):
			for y in range(self.image.shape[1]):
				pixel = self.image[x,y,:].reshape(-1)
				pixel = pixel / 255.
				pixel_hsv = colorsys.rgb_to_hsv(*pixel)
				self.elements.append(pixel_hsv[0])


