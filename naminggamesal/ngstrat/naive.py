#!/usr/bin/python

from . import BaseStrategy
import random
import numpy as np

		##################################### STRATEGIE NAIVE########################################
class StratNaive(BaseStrategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			m = random.choice(voc.get_known_meanings(w))
		else:
			if len(voc.get_known_meanings())<voc._M:
				m = voc.get_new_unknown_m()
			else:
				m = random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			w = voc.get_random_known_w(m)
		else:
			w = voc.get_new_unknown_w()
		return w

	def pick_m(self,voc,mem):
		m = random.randint(0,voc.get_M()-1)
		return m

	def hearer_pick_m(self,voc,mem):
		m = self.pick_m(voc,mem)
		return m
