#!/usr/bin/python

from .naive import StratNaive
import random
import numpy as np



##################################### STRATEGIE SUCCESS THRESHOLD########################################
class StratSuccessThreshold(StratNaive):

	def __init__(self, threshold_explo=0.9, **strat_cfg2):
		super(StratSuccessThreshold, self).__init__(**strat_cfg2)
		if 'threshold_explo' not in strat_cfg2.keys():
			self.threshold_explo=threshold_explo

	def pick_m(self,voc,mem):
		test1=self.get_success_rate_over_known_meanings(voc,mem)>self.threshold_explo
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		if (test1 or test3) and (not test2):
			m=voc.get_new_unknown_m()
		else:
			m=voc.get_random_known_m()
		return m

	def hearer_pick_m(self,voc,mem):
		return self.pick_m(voc, mem)

	def update_memory(self,ms,w,mh,voc,mem,role):
		if role=='speaker':
			m1=ms
		else:
			m1=mh
		if ms==mh:
			mem["success_m"][m1]+=1
		else:
			mem["fail_m"][m1]+=1

	def init_memory(self,voc):
		mem={}
		mem["success_m"]=[]
		mem["fail_m"]=[]
		for i in range(0,voc._M):
			mem["success_m"].append(0)
			mem["fail_m"].append(0)
		return mem

	def get_success_rate_over_known_meanings(self,voc,mem):
		succ_sum=0
		fail_sum=0
		for m in voc.get_known_meanings():
			succ_sum+=mem["success_m"][m]
			fail_sum+=mem["fail_m"][m]
		if succ_sum==0:
			return 0
		else:
			return succ_sum/float(fail_sum+succ_sum)

##################################### STRATEGIE SUCCESS THRESHOLD CORRECTED########################################
class StratSuccessThresholdCorrected(StratSuccessThreshold):

	def get_success_rate_over_known_meanings(self,voc,mem):
		succ_sum=0
		fail_sum=0
		temprate=0
		for m in voc.get_known_meanings():
			succ_sum=mem["success_m"][m]
			fail_sum=mem["fail_m"][m]
			if succ_sum!=0:
				temprate+=succ_sum/float(fail_sum+succ_sum)
		if voc.get_known_meanings():
			return temprate/len(voc.get_known_meanings())
		else:
			return 1

##################################### STRATEGIE SUCCESS THRESHOLD WISE########################################
class StratSuccessThresholdWise(StratSuccessThreshold):

	def get_success_rates(self, voc, mem):
		succ_sum = 0
		fail_sum = 0
		ratelist = []
		for m in voc.get_known_meanings():
			succ_sum=mem["success_m"][m]
			fail_sum=mem["fail_m"][m]
			if succ_sum!=0:
				ratelist.append(succ_sum/float(fail_sum+succ_sum))
			else:
				ratelist.append(0)
		return ratelist

	def pick_m(self, voc, mem):
		ratelist = self.get_success_rates(voc, mem)
		if (np.mean(ratelist)>self.threshold_explo and len(voc.get_known_meanings())<voc._M) or len(voc.get_known_meanings()) == 0 :
			return voc.get_new_unknown_m()
		tempmin = 1
		KM = voc.get_known_meanings()
		for m in range(0,len(KM)):
			tempmin = min(tempmin, ratelist[m])
		tempm = []
		for m in range(0,len(KM)):
			if ratelist[m] == tempmin:
				tempm.append(m)
		j = random.randint(0, len(tempm)-1)
		ans = KM[tempm[j]]
		return ans
