#!/usr/bin/python

from .naive import StratNaive
import random
import numpy as np



##################################### STRATEGIE SUCCESS THRESHOLD########################################
class StratMinCounts(StratNaive):

	def __init__(self, vu_cfg, mincounts=5 , **strat_cfg2):
		super(StratMinCounts, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		if 'mincounts' not in strat_cfg2.keys():
			self.mincounts=mincounts


	def hearer_pick_m(self,voc,mem, context):
		return self.pick_m(voc, mem, context)

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		StratNaive.update_memory(self,ms=ms,w=w,mh=mh,voc=voc,mem=mem,role=role,bool_succ=bool_succ)
		if role=='speaker':
			m1=ms
		else:
			m1=mh
		if bool_succ:
			mem["success_m"][m1]+=1
		else:
			mem["fail_m"][m1]+=1

	def init_memory(self,voc):
		mem = StratNaive.init_memory(self,voc=voc)
		mem["success_m"]=[0]*voc._M
		mem["fail_m"]=[0]*voc._M
		return mem

	def get_success_counts(self, voc, mem):
		succ_sum=0
		fail_sum=0
		countlist=[]
		for m in voc.get_known_meanings():
			succ_sum=mem["success_m"][m]
			fail_sum=mem["fail_m"][m]
			countlist.append(succ_sum)
		return countlist

	def pick_m(self, voc, mem, context):
		counts = self.get_success_counts(voc, mem)
		if  (len(voc.get_known_meanings())==0) or (len(voc.get_known_meanings())<voc._M and min(counts)>self.mincounts):
			return voc.get_new_unknown_m()
		KM = voc.get_known_meanings()
		tempmin = min(counts)
		tempm = []
		for m in range(0,len(KM)):
			if counts[m] == tempmin:
				tempm.append(m)
		j = random.randint(0, len(tempm)-1)
		return KM[tempm[j]]
