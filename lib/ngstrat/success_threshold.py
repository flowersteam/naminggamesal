#!/usr/bin/python
# -*- coding: latin-1 -*-

from .naive import StratNaive
import random
import numpy as np



##################################### STRATEGIE SUCCESS THRESHOLD########################################
class StratSuccessThreshold(StratNaive):
	_strattype="success_threshold"
	threshold_explo=0.9

	def pick_mw(self,voc,mem):
		test1=self.get_success_rate_over_known_meanings(voc,mem)>self.threshold_explo
		test2=len(voc.get_known_meanings())==voc._M
		test3=len(voc.get_known_meanings())==0
		if (test1 or test3) and (not test2):
			m=voc.get_new_unknown_m()
			w=voc.get_new_unknown_w()
		else:
			m=voc.get_random_known_m()
			w=self.pick_w(m,voc,mem)
		return([m,w])


	def update_hearer(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["success_m"][mh]+=1
		else:
			mem["fail_m"][mh]+=1
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		if ms==mh:
			mem["success_m"][ms]+=1
		else:
			mem["fail_m"][ms]+=1
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def init_memory(self,voc):
		mem={}
		mem["success_m"]=[0]*voc._M
		mem["fail_m"]=[0]*voc._M
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
	_strattype="success_threshold_corrected"
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


##################################### STRATEGIE SUCCESS THRESHOLD REELLE########################################
class StratSuccessThresholdReal(StratSuccessThreshold):


	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["success_m"][mh]+=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["fail_m"][mh]+=1

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			mem["success_m"][ms]+=1
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		else:
			mem["fail_m"][ms]+=1

	def init_memory(self,voc):
		mem={}
		mem["success_m"]=[0]*voc._M
		mem["fail_m"]=[0]*voc._M
		return mem
