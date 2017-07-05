
from . import BaseStrategy
import random
import numpy as np
from intervaltree import IntervalTree, Interval

		#####################################NAIVE STRATEGY########################################
class StratUser(BaseStrategy):

	def guess_m(self,w,voc,mem,context=[]):
		if w is not None:
			w_str = ' for word '+str(w)
		else:
			w_str = ''
		print 'pick a meaning'+ w_str +' from:'
		possible_choices = voc.get_accessible_meanings()
		return self.get_choice_from_list(possible_choices)

	def pick_w(self,m,voc,mem,context=[]):
		if m is not None:
			m_str = ' for meaning '+str(m)
		else:
			m_str = ''
		print 'pick a word'+ m_str +' from:'
		possible_choices = voc.get_accessible_words()
		return self.get_choice_from_list(possible_choices)

	def pick_m(self,voc,mem,context=[]):
		print 'pick a meaning from:'
		possible_choices = voc.get_accessible_meanings()
		return self.get_choice_from_list(possible_choices)

	def get_choice_from_list(self,possible_choices):
		if hasattr(possible_choices,'sorted'):
			print possible_choices.sorted()
		else:
			print possible_choices
		val = raw_input()
		if val in possible_choices:
			print 'you have chosen:',val
			return val
		elif val in [str(v) for v in possible_choices]:
			print 'you have chosen:',val
			for v in possible_choices:
				if val == str(v):
					break
			return v
		else:
			print 'Not in possible choices, reasking'
			return self.get_choice_from_list(possible_choices=possible_choices)
			#raise IOError('not in possible choices')

