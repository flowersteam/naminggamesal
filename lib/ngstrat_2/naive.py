#!/usr/bin/python
# -*- coding: latin-1 -*-

from . import BaseStrategy
import random
import numpy as np

##################################### STRATEGIE NAIVE DESTRUCTIVE################################
class StratNaiveDestructive(BaseStrategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,len(voc.get_known_meanings(w))-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			tempindexw=random.randint(0,len(voc.get_known_words(m))-1)
			w=voc.get_known_words(m)[tempindexw]
		else:
			w=random.randint(0,voc.get_W()-1)
		return w


	def pick_mw(self,voc,mem):
		m=random.randint(0,voc.get_M()-1)
		w=self.pick_w(m,voc,mem)
		return([m,w])

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		return {}

		##################################### STRATEGIE NAIVE########################################
class StratNaive(BaseStrategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,len(voc.get_known_meanings(w))-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			if len(voc.get_known_meanings())<voc._M:
				m=voc.get_new_unknown_m()
			else:
				m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			w=voc.get_random_known_w(m)
		else:
			w=voc.get_new_unknown_w()
		return w


	def pick_mw(self,voc,mem):
		m=random.randint(0,voc.get_M()-1)
		w=self.pick_w(m,voc,mem)
		return([m,w])

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		return {}

		##################################### STRATEGIE NAIVE REELLE########################################
class StratNaiveReal(BaseStrategy):

	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,len(voc.get_known_meanings(w))-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			if len(voc.get_known_meanings())<voc._M:
				m=voc.get_new_unknown_m()
			else:
				m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			w=voc.get_random_known_w(m)
		else:
			w=voc.get_new_unknown_w()
		return w


	def pick_mw(self,voc,mem):
		m=random.randint(0,voc.get_M()-1)
		w=self.pick_w(m,voc,mem)
		return([m,w])

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)

	def init_memory(self,voc):
		return {}
