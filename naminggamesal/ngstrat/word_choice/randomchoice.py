##
from . import BaseWordChoice

class RandomWordChoice(BaseWordChoice):

	def pick_w(self,m,voc,mem,context=[]):
		if m in voc.get_known_meanings():
			w = voc.get_random_known_w(m=m)
		elif voc.get_unknown_words():
			w = voc.get_new_unknown_w()
		else:
			w = voc.get_random_known_w(option='min')
		return w
