#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module
import copy

from .success import get_success
from .voc_update import get_voc_update
from .word_choice import get_wordchoice

sns.set(rc={'image.cmap': 'Purples_r'})

strat_class={
	'naive':'naive.StratNaive',
	'naive_membased':'naive.StratNaiveMemBased',
	'naive_explobiased':'naive.StratNaiveExploBiased',
	'naive_membased_explobiased':'naive.StratNaiveMemBasedExploBiased',
	'naive_category':'naive.StratNaiveCategory',
	'naive_category_pone':'naive.StratNaiveCategoryPlosOne',

	'only_explore':'naive.StratOnlyExplore',
	'only_exploit':'naive.StratOnlyExploit',

	'success_threshold':'success_threshold.StratSuccessThreshold',
	'success_threshold_epirob':'success_threshold.StratSuccessThresholdEpirob',
	# 'success_threshold_corrected':'success_threshold.StratSuccessThresholdCorrected',
	'success_threshold_wise':'success_threshold.StratSuccessThresholdWise',
	'success_threshold_wise_only2ndlevel':'success_threshold.StratSuccessThresholdWiseOnly2ndLevel',
	'success_threshold_wise_partially_naive':'success_threshold.StratSuccessThresholdWisePartiallyNaive',
	'success_threshold_wise_max':'success_threshold.StratSuccessThresholdWiseMax',
	'success_threshold_scores':'success_threshold.StratSuccessThresholdScores',

	'category_success_threshold':'category_success_threshold.CategorySuccessThresholdStrat',
	'category_st_distance':'category_success_threshold.CategoryDistanceSTStrat',
	'category_st_dist_strict':'category_success_threshold.DistSTStrict',
	'category_st_distcenter':'category_success_threshold.CategoryDistCenterStrat',
	'category_dist_successgoal': 'category_success_threshold.DistSuccessGoal',
	'category_center_successgoal': 'category_success_threshold.CenterSuccessGoal',
	'category_dc_successgoal': 'category_success_threshold.DCSuccessGoal',
	'category_dist_successslope': 'category_success_threshold.DistSuccessSlope',
	'category_center_successslope': 'category_success_threshold.CenterSuccessSlope',
	'category_dc_successslope': 'category_success_threshold.DCSuccessSlope',


	'mincounts':'mincounts.StratMinCounts',
	'mincounts_mean':'mincounts.StratMinCountsMean',
	'mincounts_basic':'mincounts.StratMinCountsBasic',
	'mincounts_wise_max':'mincounts.StratMinCountsWiseMax',
	'mincounts_only2ndlevel':'mincounts.StratMinCountsOnly2ndLevel',

	'decision_vector':'decision_vector.StratDecisionVector',
	'decision_vector_gainmax':'decision_vector.StratDecisionVectorGainmax',
	'decision_vector_gainsoftmax':'decision_vector.StratDecisionVectorGainSoftmax',
	'decision_vector_chunks':'decision_vector.StratDecisionVectorChunks',

	'decision_vector_gainsoftmax_hearer':'decision_vector.StratDecisionVectorGainSoftmaxHearer',

	'decision_vector_gainsoftmax_hearer_test':'decision_vector.StratDecisionVectorGainSoftmaxHearerTest',

	'last_result':'last_result.StratLastResult',
	'omniscient':'omniscient.StratOmniscient',

	'tsrmax':'tsrmax.StratTSRMax',
	'tsrmax_mab':'tsrmax.StratTSRMaxMAB',
	'tsrmax_hmab':'tsrmax.StratTSRMaxHMAB',

	'lapsmax_mab':'tsrmax.LAPSMaxMAB',
	'lapsmax_mab_explothreshold':'tsrmax.LAPSMaxMABExploThreshold',
	'negentropymax_mab_explothreshold':'tsrmax.NegentropyMaxMABExploThreshold',
	'lapsmax_mab_explothreshold_only2ndlevel':'tsrmax.LAPSMaxMABExploThresholdOnly2ndLevel',
	'negentropymax_mab_explothreshold_only2ndlevel':'tsrmax.NegentropyMaxMABExploThresholdOnly2ndLevel',

	'user':'user.StratUser',
	'user_noninteractive':'user.StratUserNonInteractive',

	'coherence':'coherence_counts.StratCoherence',
	'coherence_last':'coherence_counts.StratCoherenceLast',
	'coherence_last_only2ndlevel':'coherence_counts.StratCoherenceLastOnly2ndLevel',
	'coherence_new':'coherence_counts.StratCoherenceNew',
}

def get_strategy(strat_type='naive', vu_cfg={}, success_cfg={}, wordchoice_cfg={}, **strat_cfg2):
	tempstr = strat_type
	if tempstr == 'mixed':
		tot = sum(strat_cfg2['proba'])
		r = random.random()*tot
		p=strat_cfg2['proba'][0]
		i=0
		while r>p:
			p += strat_cfg2['proba'][i+1]
			i += 1
		return get_strategy(**strat_cfg2['cfg_list'][i])
	if tempstr in list(strat_class.keys()):
		tempstr = strat_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	strat = getattr(_tempmod,tempclass)(vu_cfg=vu_cfg, success_cfg=success_cfg, wordchoice_cfg=wordchoice_cfg, **strat_cfg2)
	strat.strat_type = strat_type
	return strat


class BaseStrategy(object):

	def __init__(self, vu_cfg={}, success_cfg={}, wordchoice_cfg={}, allow_idk=False, memory_policies=[], **strat_cfg2):
		#for key, value in strat_cfg2.iteritems():
		#	setattr(self, key, value)
		self.allow_idk = allow_idk
		self.voc_update = get_voc_update(**vu_cfg)
		self.memory_policies = copy.deepcopy(memory_policies)
		self.wordchoice = get_wordchoice(**wordchoice_cfg)
		if 'successcount' not in [mp['mem_type'] for mp in self.memory_policies]:
			self.memory_policies.append({'mem_type':'successcount'})
		# if 'inventions' not in [mp['mem_type'] for mp in self.memory_policies]:
		# 	self.memory_policies.append({'mem_type':'inventions'})
		if hasattr(self.voc_update,'memory_policies'):
			for mp in self.voc_update.memory_policies:
				if sum([ (mp['mem_type'] not in mmpp['mem_type']) for mmpp in self.memory_policies]):
					self.memory_policies.append(copy.deepcopy(mp))
		if hasattr(self.wordchoice,'memory_policies'):
			for mp in self.wordchoice.memory_policies:
				if sum([ (mp['mem_type'] not in mmpp['mem_type']) for mmpp in self.memory_policies]):
					self.memory_policies.append(copy.deepcopy(mp))
		self.success = get_success(**success_cfg)

	def update_speaker(self, ms, w, mh, voc, mem, bool_succ, context=[]):
		if not hasattr(self,'broadcasting') or not self.voc_update.broadcasting:
			return self.voc_update.update_speaker(ms, w, mh, voc, mem, bool_succ, context)

	def update_hearer(self, ms, w, mh, voc, mem, bool_succ, context=[]):
		return self.voc_update.update_hearer(ms, w, mh, voc, mem, bool_succ, context)

#	def init_memory(self,voc):
#		mem = {}
#		mem['success'] = 0
#		mem['fail'] = 0
#		return mem
#
#	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
#		if bool_succ:
#			mem['success'] += 1
#		else:
#			mem['fail'] += 1

	def get_strattype(self):
		return self._strattype

	def visual(self, voc, mem={}, vtype=None, iterr=100, mlist="all", wlist="all"):
		if mlist=="all":
			mlist=list(range(0,voc._M))
		if wlist=="all":
			wlist=list(range(0,voc._W))
		if vtype=="pick_mw":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for i in range(0,iterr):
				lst=self.pick_mw(voc,mem)
				j=lst[0]
				k=lst[1]
				tempmat[j,k]+=1
			plt.figure()
			plt.title("pick_mw")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype=="pick_m":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for i in range(0,iterr):
				lst=self.pick_mw(voc,mem)
				j=lst[0]
				for k in range(0,voc._W):
					tempmat[j,k]+=1
			plt.figure()
			plt.title("pick_m")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype=="pick_w":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for m in mlist:
				for i in range(0,iterr):
					lst=self.pick_w(m,voc,mem)
					j=m
					k=lst
					tempmat[j,k]+=1
			plt.figure()
			plt.title("pick_w")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype=="guess_m":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for w in wlist:
				for i in range(0,iterr):
					lst=self.guess_m(w,voc,mem)
					j=lst
					k=w
					tempmat[j,k]+=1
			plt.figure()
			plt.title("guess_m")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype==None:
			voc.visual()
		elif vtype=="syn":
			voc.visual(vtype="syn")
		elif vtype=="hom":
			voc.visual(vtype="hom")

	def pick_mw(self,voc,mem,context=[]):
		m = self.pick_m(voc,mem,context)
		w = self.pick_w(m,voc,mem,context)
		return [m,w]

	def pick_m(self,voc,mem,context=[]):
		pass

	def pick_w(self,m,voc,mem,context=[]):
		return self.wordchoice.pick_w(m=m,voc=voc,mem=mem,context=context)

	def guess_m(self,voc,mem,context=[]):
		pass
