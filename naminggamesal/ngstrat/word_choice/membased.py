import numpy as np

from . import BaseWordChoice

class MemBasedWordChoice(BaseWordChoice):

	def pick_w(self,m,voc,mem,context=[]):
		if m in voc.get_known_meanings() and voc.get_known_words(m=m,option=None):
			w_list = voc.get_known_words(m=m,option=None)
			if 'interact_count_voc' in list(mem.keys()):
				p_list = [ mem['interact_count_voc'].get_value(m=m,w=w1,content_type='m') for w1 in w_list]
				p = np.asarray(p_list)
				p = p/p.sum()
				if p.sum() != 1:
					w = voc.get_random_w(w_list)
				else:
					w = np.random.choice(w_list,p=p)
				if w not in voc.get_known_words(m=m):
					w = voc.get_random_known_w(m=m)
			else:
				w = voc.get_random_w(w_list)
		elif voc.get_unknown_words():
			w = voc.get_new_unknown_w()
		else:
			w = voc.get_random_known_w(option='min')
		return w
