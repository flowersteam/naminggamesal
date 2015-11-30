#!/usr/bin/python

from . import BaseStrategy
import random
import numpy as np

		##################################### STRATEGIE NAIVE########################################
class StratNaive(BaseStrategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			m = voc.get_random_known_m(w)
		elif voc.get_unknown_meanings():
			m = voc.get_new_unknown_m()
		else:
			m = random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			w = voc.get_random_known_w(m)
		elif voc.get_unknown_words():
			w = voc.get_new_unknown_w()
		else:
			w = random.randint(0,voc.get_W()-1)
		return w

	def pick_m(self,voc,mem):
		m = random.randint(0,voc.get_M()-1)
		return m

	def hearer_pick_m(self,voc,mem):
		m = self.pick_m(voc,mem)
		return m
