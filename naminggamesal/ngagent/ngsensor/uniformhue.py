from . import SensoryApparatus

class UniformHueSA(SensoryApparatus):
	def __init__(self, env=None, d_min=0.01):
		SensoryApparatus.__init__(self)
		self.d_min = d_min

	def discriminable(self, input_sig1, input_sig2):
		if abs(input_sig1 - input_sig2) >= self.d_min:
			return True
		else:
			return False
