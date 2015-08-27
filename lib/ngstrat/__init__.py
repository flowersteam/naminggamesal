#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
strat_class={
	'naive':'naive.StratNaive',
	'naive_destructive':'naive.StratNaiveDestructive',

	'success_threshold':'success_threshold.StratSuccessThreshold',
	'success_threshold_corrected':'success_threshold.StratSuccessThresholdCorrected',
	'success_threshold_wise':'success_threshold.StratSuccessThresholdWise',

	'mincounts':'mincounts.StratMinCounts',

	'decision_vector':'decision_vector.StratDecisionVector',
	'decision_vector_gainmax':'decision_vector.StratDecisionVectorGainmax',
	'decision_vector_gainsoftmax':'decision_vector.StratDecisionVectorGainSoftmax',

	'last_result':'last_result.StratLastResult'
}

def Strategy(strat_type='naive', voc_update='Adaptive', **strat_cfg2):
	tempstr = strat_type
	if tempstr in strat_class.keys():
		tempstr = strat_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	_tempmod2 = import_module('.voc_update_decorators',package=__name__)
	tempstrat = getattr(_tempmod,tempclass)(**strat_cfg2)
	return getattr(_tempmod2,voc_update)(tempstrat)


class BaseStrategy(object):

	def __init__(self, **strat_cfg2):
		for key, value in strat_cfg2.iteritems():
			setattr(self, key, value)

	def get_strattype(self):
		return self._strattype

	def visual(self, voc, mem={}, vtype=None, iterr=100, mlist="all", wlist="all"):
		if mlist=="all":
			mlist=range(0,voc._M)
		if wlist=="all":
			wlist=range(0,voc._W)
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
