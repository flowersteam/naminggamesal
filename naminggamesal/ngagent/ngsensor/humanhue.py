
from . import SensoryApparatus


class HumanHueSA(SensoryApparatus):

	def d_min(self, h):
		raise Exception('not implemented')


	def discriminable(self, input_sig1, input_sig2):
		if abs(input_sig1 - input_sig2) >= max(self.d_min(input_sig1),self.d_min(input_sig2)):
			return True
		else:
			return False
