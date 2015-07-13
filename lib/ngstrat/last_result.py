#!/usr/bin/python
# -*- coding: latin-1 -*-

from .naive import StratNaive
from .naive import StratNaiveReal
import random
import numpy as np



##################################### STRATEGIE LAST_RESULT########################################
class StratLastResult(StratNaive):

	def pick_mw(self,voc,mem):
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		#if (mem["result"] or test3) and (not test2):
		if mem["result"]:
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["result"]=1
		else:
			mem["result"]=0
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["result"]=1
		else:
			mem["result"]=0
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		mem={}
		mem["result"]=1
		return mem

##################################### STRATEGIE LAST_RESULT REELLE########################################
class StratLastResultReal(StratNaiveReal):

	def pick_mw(self,voc,mem):
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		if (mem["result"] or test3) and (not test2):
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["result"]=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["result"]=0

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["result"]=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["result"]=0

	def init_memory(self,voc):
		mem={}
		mem["result"]=1
		return mem
