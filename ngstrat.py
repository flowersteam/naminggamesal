#!/usr/bin/python
# -*- coding: latin-1 -*-

class Strategy(object):
	def __new__(cls,strattype):
		if strattype=="naive":
			return object.__new__(StratNaive)
		if strattype=="delaunay":
			return object.__new__(StratDelaunay)
	def get_strattype(self):
		return _strattype


class StratNaive(Strategy):
	_strattype="naive"

	def pick_mw(self,voc,mem):

	def pick_new_m(self,voc,mem):

	def guess_m(self,w,voc,mem):

	def pick_w(self,m,voc,mem):

	def update_hearer(self,ms,w,mh,voc,mem):

	def update_speaker(self,ms,w,mh,voc,mem):

	def init_memory(self,voc):
		return {}

class StratDelaunay(StratNaive):
	_strattype="delaunay"