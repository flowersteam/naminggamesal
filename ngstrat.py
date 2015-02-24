#!/usr/bin/python
# -*- coding: latin-1 -*-
import random
from ngvoc import *

class Strategy(object):
	def __new__(cls,strattype):
		if strattype=="naive":
			return object.__new__(StratNaive)
		elif strattype=="delaunay":
			return object.__new__(StratDelaunay)
		else:
			print "type de strategie non existant"	
	def get_strattype(self):
		return _strattype


class StratNaive(Strategy):
	_strattype="naive"


	def guess_m(self,w,voc,mem):
		if w in voc.get_known_words():
			tempindexm=random.randint(0,voc.get_known_meanings(w).length()-1)
			m=voc.get_known_meanings(w)[tempindexm]
		else:
			m=random.randint(0,voc.get_M()-1)
		return m

	def pick_w(self,m,voc,mem):
		if m in voc.get_known_meanings():
			tempindexw=random.randint(0,voc.get_known_words(m).length()-1)
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

class StratDelaunay(StratNaive):
	_strattype="delaunay"


if __name__ == "__main__":
	print "main"
	test=ngstrat.Strategy("naive")
	voc=ngstrat.Vocabulary("matrix",5,8)
	test.pick_mw(voc,{})