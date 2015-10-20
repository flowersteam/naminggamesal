#!/usr/bin/python
# -*- coding: latin-1 -*-

from .naive import StratNaive
import random
import numpy as np



##################################### STRATEGIE LAST_RESULT########################################
class StratLastResult(StratNaive):

	def pick_m(self,voc,mem):
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		#if (mem["result"] or test3) and (not test2):
		if mem["result"]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		return m

	def hearer_pick_m(self,voc,mem):
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		#if (mem["result"] or test3) and (not test2):
		if mem["result"]:
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		return m,w

	def update_memory(self,ms,w,mh,voc,mem,role='speaker'):
		if ms==mh:
			mem["result"]=1
		else:
			mem["result"]=0

	def init_memory(self,voc):
		mem={}
		mem["result"]=1
		return mem
