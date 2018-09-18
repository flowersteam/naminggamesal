#!/usr/bin/python
from __future__ import division

from .naive import StratNaive
import random
import numpy as np


##################################### STRATEGY SUCCESS THRESHOLD########################################
class StratSuccessThreshold(StratNaive):

	def __init__(self, vu_cfg, threshold_explo=0.9, **strat_cfg2):
		super(StratSuccessThreshold, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		self.threshold_explo = threshold_explo
		mp = {'mem_type':'successcount_perm'}
		if sum([ (mp['mem_type'] not in mmpp['mem_type']) for mmpp in self.memory_policies]):
			self.memory_policies.append(mp)

	def pick_m(self,voc,mem,context):
		test1 = self.get_success_rate_over_known_meanings(voc,mem)>self.threshold_explo
		test2 = len(voc.get_known_meanings())==voc.get_M()
		test3 = len(voc.get_known_meanings())==0
		if (test1 or test3) and (not test2):
			m = voc.get_new_unknown_m()
		else:
			m = voc.get_random_known_m()
		return m

	def hearer_pick_m(self,voc,mem,context):
		return self.pick_m(voc, mem,context)

#	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
#		StratNaive.update_memory(self,ms=ms,w=w,mh=mh,voc=voc,mem=mem,role=role,bool_succ=bool_succ)
#		if role=='speaker':
#			m1=ms
#		else:
#			m1=mh
#		if bool_succ:
#			mem["success_m"][m1]+=1
#		else:
#			mem["fail_m"][m1]+=1
#
#	def init_memory(self,voc):
#		mem = StratNaive.init_memory(self,voc)
#		mem["success_m"]=[]
#		mem["fail_m"]=[]
#		for i in range(0,voc._M):
#			mem["success_m"].append(0)
#			mem["fail_m"].append(0)
#		return mem

	def div(self,a,b):
		try:
			return a/b
		except:
			return 0.

	def get_success_rate_over_known_meanings(self,voc,mem):
		succ_sum = 0
		fail_sum = 0
		ratelist = []
		KM = voc.get_known_meanings()
		try:
			ratelist = [self.div(mem["success_m"][m],mem["fail_m"][m]) for m in KM]
		except KeyError:
			ratelist = np.zeros((len(KM),))
		if KM:
			return np.mean(ratelist)
		else:
			return 1.
		# succ_sum=0
		# fail_sum=0
		# temprate=0
		# for m in voc.get_known_meanings():
		# 	try:
		# 		succ_sum=mem["success_m"][m]
		# 	except KeyError:
		# 		succ_sum = 0
		# 	try:
		# 		fail_sum=mem["fail_m"][m]
		# 	except KeyError:
		# 		fail_sum = 0
		# 	if succ_sum!=0:
		# 		temprate+=succ_sum/float(fail_sum+succ_sum)
		# if voc.get_known_meanings():
		# 	return temprate/len(voc.get_known_meanings())
		# else:
		# 	return 1

##################################### STRATEGY SUCCESS THRESHOLD WISE########################################
class StratSuccessThresholdWise(StratSuccessThreshold):

	def get_success_rates(self, voc, mem):
		succ_sum = 0
		fail_sum = 0
		ratelist = []
		KM = voc.get_known_meanings()
		try:
			ratelist = [self.div(mem["success_m"][m],mem["fail_m"][m]) for m in KM]
		except KeyError:
			ratelist = np.zeros((len(KM),))
		return ratelist

	def pick_m(self, voc, mem, context):
		ratelist = self.get_success_rates(voc, mem)
		KM = voc.get_known_meanings()
		if len(KM) == 0 or (np.mean(ratelist)>self.threshold_explo and len(KM)<voc.get_M()) :
			return voc.get_new_unknown_m()
		tempmin = min(ratelist)
		# tempm = []
		# for m in range(0,len(KM)):
		# 	if ratelist[m] == tempmin:
		# 		tempm.append(m)
		# try:
		# 	meaning_list = [KM[m] for m in tempm]
		try:
			meaning_list = [m for m,r in zip(KM,ratelist) if r == tempmin]
			return voc.get_random_m(m_list=meaning_list)
		except IndexError:
			return voc.get_random_known_m()
##################################### STRATEGY SUCCESS THRESHOLD WISE PARTIALLY NAIVE########################################
class StratSuccessThresholdWisePartiallyNaive(StratSuccessThresholdWise):

	def __init__(self,proba_naive,*args,**kwargs):
		self.proba_naive = proba_naive
		StratSuccessThresholdWise.__init__(self,*args,**kwargs)

	def pick_m(self, voc, mem, context):
		if np.random.random() <= self.proba_naive:
			return StratNaive.pick_m(self, voc=voc, mem=mem, context=context)
		else:
			return StratSuccessThresholdWise.pick_m(self, voc=voc, mem=mem, context=context)


##################################### STRATEGY SUCCESS THRESHOLD WISE MAX########################################
class StratSuccessThresholdWiseMax(StratSuccessThresholdWise):

	def pick_m(self, voc, mem, context):
		ratelist = self.get_success_rates(voc, mem)
		threshold = self.threshold_explo
		KM = voc.get_known_meanings()
		if len(KM) == 0:
			return voc.get_new_unknown_m()
		tempmin = np.min(ratelist)
		if (tempmin>self.threshold_explo):
			tempmax = tempmin
		else:
			tempmax = max([r for r in ratelist if r < threshold])
		try:
			meaning_list = [m for m,r in zip(KM,ratelist) if r == tempmax ]
			return voc.get_random_m(m_list=meaning_list)
		except IndexError:
			return voc.get_random_known_m()

##################################### STRATEGY SUCCESS THRESHOLD WISE########################################
class StratSuccessThresholdScores(StratSuccessThresholdWise):

	def __init__(self, vu_cfg, **strat_cfg2):
		StratSuccessThresholdWise.__init__(self,vu_cfg=vu_cfg, **strat_cfg2)
		mp = {'mem_type':'successcount_permw'}
		if sum([ (mp['mem_type'] not in mmpp['mem_type']) for mmpp in self.memory_policies]):
			self.memory_policies.append(mp)
#	def init_memory(self,voc):
#		mem = StratNaive.init_memory(self,voc)
#		mem["success_m"] = np.zeros((voc._M, voc._W))
#		mem["fail_m"] = np.zeros((voc._M, voc._W))
#		return mem
#
#	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
#		StratNaive.update_memory(self,ms=ms,w=w,mh=mh,voc=voc,mem=mem,role=role,bool_succ=bool_succ)
#		if role=='speaker':
#			m1 = ms
#		else:
#			m1 = mh
#		if bool_succ:
#			mem["success_m"][m1, w]+=1
#		else:
#			mem["fail_m"][m1, w]+=1

	def get_success_rates(self, voc, mem):
		with np.errstate(divide='ignore', invalid='ignore'):
			c = np.true_divide(mem['success_mw'],mem['success_mw'] + mem['fail_mw'])
			c[c == np.inf] = 0
			c = np.nan_to_num(c)
		rates = np.multiply(voc.get_content(), c).sum(axis = 1)
		ratelist = [rates[m]/len(voc.get_known_words(m)) for m in voc.get_known_meanings()]
		return ratelist

##################################### STRATEGY SUCCESS THRESHOLD EPIROB########################################
class StratSuccessThresholdEpirob(StratNaive):

	def __init__(self, vu_cfg, threshold_explo=0.9, proba_new_m=0.001,proba_2=0.1,**strat_cfg2):
		super(StratSuccessThresholdEpirob, self).__init__(vu_cfg=vu_cfg, **strat_cfg2)
		self.threshold_explo = threshold_explo
		self.proba_new_m = proba_new_m
		self.proba_2 = proba_2

	def pick_m(self,voc,mem,context):
		test1 = self.get_bestscores_mean(voc,mem) > self.threshold_explo
		test2 = len(voc.get_known_meanings()) == voc.get_M()
		test3 = len(voc.get_known_meanings()) == 0
		test4 = random.random() < self.proba_new_m
		test5 = random.random() < self.proba_2
		if (test1 and not test2) or (test4 and not test2):
			m = voc.get_new_unknown_m()
		else:
			if not test3:
				if test5:
					m = self.get_lowest_score_m(voc,mem)
				else:
					m = voc.get_random_known_m()
			else:
				m = voc.get_new_unknown_m()
		return m

	def hearer_pick_m(self,voc,mem,context):
		return self.pick_m(voc, mem,context)

	def get_bestscores_mean(self,voc,mem):
		BS = []
		for m in voc.get_known_meanings():
			BS.append(0)
			w_l = []
			for w in voc.get_known_words(m=m):
				BS[-1] = max(voc.get_value(m,w),BS[-1])
		if not BS:
			return 0
		else:
			return np.mean(BS)

	def get_lowest_score_m(self,voc,mem):
		LS = 1.
		m_l = []
		for m in voc.get_known_meanings():
			for w in voc.get_known_words(m=m):
				if voc.get_value(m,w) < LS:
					m_l = [m]
				elif voc.get_value(m,w) == LS:
					m_l.append(m)
		m_l = list(set(m_l))
		return voc.get_random_m(m_l)
