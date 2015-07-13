#!/usr/bin/python
# -*- coding: latin-1 -*-
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
strat_class={
	'naive':'naive.StratNaive',
	'naive_real':'naive.StratNaiveReal',
	'naive_destructive':'naive.StratNaiveDestructive',

	'success_threshold':'success_threshold.StratSuccessThreshold',
	'success_threshold_corrected':'success_threshold.StratSuccessThresholdCorrected',
	'success_threshold_real':'success_threshold.StratSuccessThresholdReal',

	'decision_vector':'decision_vector.StratDecisionVector',
	'decision_vector_real':'decision_vector.StratDecisionVectorReal',

	'last_result':'last_result.StratLastResult',
	'last_result_real':'last_result.StratLastResultReal'
}

def Strategy(strat_type='naive', **strat_cfg2):
	tempstr = strat_type
	if tempstr in strat_class.keys():
		tempstr = strat_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempstrat = getattr(_tempmod,tempclass)(**strat_cfg2)
	return tempstrat


class BaseStrategy(object):

	def __init(self, **strat_cfg2):
		for key, value in kwargs.iteritems():
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




#
#		elif _strattype[:13]=="delaunaymodif":
#			tempstrat=object.__new__(StratDelaunay)
#			tempstrat.threshold_explo=float(_strattype[13:])
#			tempstrat._strattype=_strattype
#			return tempstrat
#		elif _strattype=="dichotomie":
#			tempstrat=object.__new__(StratDecisionVector)
#			tempdecvec=np.zeros(M+1)
#			tempdecvec[0]=1
#			temp_param=2
#			for i in range(1,int(np.log(M)/np.log(temp_param))+1):
#				tempdecvec[-1-M/(temp_param**i)]=1
#			tempstrat.decision_vector=tempdecvec
#			tempstrat._strattype=_strattype
#			return tempstrat
#		elif _strattype[:17]=="dichotomierapport":
#			tempstrat=object.__new__(StratDecisionVector)
#			tempdecvec=np.zeros(M+1)
#			tempdecvec[0]=1
#			temp_param=float(_strattype[17:])
#			for i in range(1,int(np.log(M)/np.log(temp_param))+1):
#				tempdecvec[-1-int(M/(temp_param**i))]=1
#			tempstrat.decision_vector=tempdecvec
#			tempstrat._strattype=_strattype
#			return tempstrat
#



