#!/usr/bin/python
import copy
import numpy as np
import math
import random
import networkx as nx
from intervaltree import IntervalTree,Interval
import scipy
from scipy.optimize import curve_fit
from scipy.special import zetac

#from numpy.linalg import norm

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph
from .ngpop import Population

from .ngmeth_utils import zipf_utils,decvec_utils,nx_utils,srtheo_utils

def pop_ize(func):
	def out_func(pop,**kwargs):
		tempNlist=[]
		agentlist=pop._agentlist
		for i in range(0,len(agentlist)):
			tempNlist.append(func(agentlist[i]))
		mean=np.mean(tempNlist)
		std=np.std(tempNlist)
		_min=np.min(tempNlist)
		_max=np.max(tempNlist)
		return [mean,std,_min,_max,tempNlist]
	out_func.__name__=func.__name__+"_mean"
	return out_func

def meaning_pop_ize(func):
	def out_func(pop,**kwargs):
		tempNlist=[]
		mlist = pop._agentlist[0]._vocabulary.get_accessible_meanings()# get from pop.env?
		for m in mlist:
			tempNlist.append(func(m=m,pop=pop))
		mean=np.mean(tempNlist)
		std=np.std(tempNlist)
		_min=np.min(tempNlist)
		_max=np.max(tempNlist)
		return [mean,std,_min,_max,tempNlist]
	out_func.__name__=func.__name__+"_mean"
	return out_func


############################	LEVEL AGENT ############################

####	INPUT:		agent , **progress_info
####	OUTPUT:		[mean,std,(tempNlist)]

#	FUNC_BIS=pop_ize(FUNC)
#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Nlink##########

def Nlink(agent,**kwargs):
	if hasattr(agent._vocabulary,'_content'):
		tempmat = copy.deepcopy(agent.get_vocabulary_content())
		tempmat[tempmat>0] = 1
		return np.sum(tempmat)
	else:
		ans = 0
		for m in agent._vocabulary.get_known_meanings():
			ans += len(agent._vocabulary.get_known_words(m=m))
		return ans

def Nlink_max(pop):
	return pop.get_M() * pop.get_W()

def Nlink_min(pop):
	return 0


FUNC=Nlink
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Nlink_min}#,"ymax":Nlink_max}
custom_Nlink =custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########nb_inventions_per_agent##########

def nb_inventions_per_agent(agent,**kwargs):
	if 'inventions' in list(agent._memory.keys()):
		return agent._memory['inventions']['nb_inventions']
	else:
		return 0

def nb_inventions_per_agent_max(pop):
	return pop.get_M()

def nb_inventions_per_agent_min(pop):
	return 0


FUNC=nb_inventions_per_agent
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":nb_inventions_per_agent_min}#,"ymax":nb_inventions_per_agent_max}
custom_nb_inventions_per_agent =custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########success_rate##########

def success_rate(agent,**kwargs):
	if agent.success+agent.fail!=0:
		return agent.success/float(agent.success+agent.fail)
	else:
		return 0

def success_rate_max(pop):
	return 1

def success_rate_min(pop):
	return 0

FUNC=success_rate
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":success_rate_min,"ymax":success_rate_max}
custom_success_rate=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########had_success##########

def had_success(agent,**kwargs):
	if agent.success>0:
		return 1.
	else:
		return 0.

def had_success_max(pop):
	return 1.

def had_success_min(pop):
	return 0.

FUNC=had_success
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":had_success_min,"ymax":had_success_max}
custom_had_success=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########new_entropy##########

def new_entropy(agent=None,mem=None,voc=None,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary

	total = mem['success_mw'] + mem['fail_mw']

	normalized0 = total.sum(axis=0, keepdims=True)
	normalized0 = np.where(normalized0!=0,total/normalized0,0.)
	entr0 = scipy.special.entr(normalized0).sum()#.sum(axis=0)

	normalized1 = total.sum(axis=1, keepdims=True)
	normalized1 = np.where(normalized1!=0,total/normalized1,0.)
	entr1 = scipy.special.entr(normalized1).sum()#.sum(axis=1)

	return entr0 + entr1




#def new_entropy_max(pop):
#	return 1

def new_entropy_min(pop):
	return 0

FUNC=new_entropy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":new_entropy_min}#,"ymax":new_entropy_max}
custom_new_entropy=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["success_mw"],**graphconfig)
#########entropy_time_scale##########

def entropy_time_scale(agent=None,mem=None,voc=None,m=None,w=None,valmax=1.,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary
	entr = 0.
	if 'interact_count_m' in list(mem.keys()):

		if m is None:
			mat = mem['interact_count_m']
		else:
			mat = mem['interact_count_m'][m,:]
		sumvec = mat.sum(axis=1)
		if voc is None:
			KW =  mem['interact_count_m'].shape[1]
		else:
			KW = voc.get_W()#len(voc.get_known_words())
		deltavec = (valmax - sumvec)/KW
		mat += deltavec

		entr +=  scipy.special.entr(mat).sum()

		if w is None:
			mat = mem['interact_count_w']
		else:
			mat = mem['interact_count_w'][:,w]
		sumvec = mat.sum(axis=0)
		if voc is None:
			KM =  mem['interact_count_m'].shape[0]
		else:
			KM = voc.get_M()
		deltavec = (valmax - sumvec)/KM
		mat += deltavec
		entr +=  scipy.special.entr(mat).sum()

		return entr
	elif 'interact_count_voc' in list(mem.keys()):
		pop_voc = mem['interact_count_voc']
		for m in pop_voc.get_known_meanings():
			temp_vec = []
			for w in pop_voc.get_known_words(m=m):
				temp_vec.append(pop_voc.get_value(m,w))
			temp_ndarray = np.ndarray(temp_vec)
			sumvec = temp_ndarray.sum()
			delta = (1.-sumvec)/pop_voc.get_W()
			temp_ndarray += delta
			entr += scipy.special.entr(temp_ndarray).sum()
			entr += (pop_voc.get_W()-len(temp_vec))*scipy.special.entr(delta)
		for w in pop_voc.get_known_words():
			temp_vec = []
			for m in pop_voc.get_known_meanings(w=w):
				temp_vec.append(pop_voc.get_value(m,w,content_type='w'))
			temp_ndarray = np.ndarray(temp_vec)
			sumvec = temp_ndarray.sum()
			delta = (1.-sumvec)/pop_voc.get_M()
			temp_ndarray += delta
			entr += scipy.special.entr(temp_ndarray).sum()
			entr += (pop_voc.get_M()-len(temp_vec))*scipy.special.entr(delta)

		return entr

	else:
		return 0




#def entropy_time_scale_max(pop):
#	return 1

def entropy_time_scale_min(pop):
	return 0

FUNC=entropy_time_scale
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":entropy_time_scale_min}#,"ymax":entropy_time_scale_max}
custom_entropy_time_scale=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)
#########new_entropy_success##########

def new_entropy_success(agent=None,mem=None,voc=None,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary

	success = mem['success_mw']

	normalized0 = success.sum(axis=0, keepdims=True)
	normalized0 = np.where(normalized0!=0,success/normalized0,0.)
	entr0 = scipy.special.entr(normalized0).sum()#.sum(axis=0)

	normalized1 = success.sum(axis=1, keepdims=True)
	normalized1 = np.where(normalized1!=0,success/normalized1,0.)
	entr1 = scipy.special.entr(normalized1).sum()#.sum(axis=1)

	return entr0 + entr1




#def new_entropy_success_max(pop):
#	return 1

def new_entropy_success_min(pop):
	return 0

FUNC=new_entropy_success
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":new_entropy_success_min}#,"ymax":new_entropy_max}
custom_new_entropy_success=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["success_mw"],**graphconfig)

#########new_entropy_withvoc##########

def new_entropy_withvoc(agent=None,mem=None,voc=None,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary

	success = mem['success_mw']
	fail = mem['fail_mw']
	total = success + fail

	#normalized0 = total.sum(axis=0, keepdims=True)
	#normalized0 = np.where(normalized0!=0,total/normalized0,0.)
	#own_assoc0 = np.where(voc._content!=0,normalized0,0.)
	#others0 = normalized0-own_assoc0

	total = np.where(voc._content!=0,total,0.)

	norm0 = total.sum(axis=0, keepdims=True)
	normalized0 = np.where(total!=0,total/norm0,0.)
	entr0 = scipy.special.entr(normalized0).sum()#.sum(axis=0)

	norm1 = total.sum(axis=1, keepdims=True)
	normalized1 = np.where(norm1!=0,total/norm1,0.)
	entr1 = scipy.special.entr(normalized1).sum()#.sum(axis=0)


	#normalized1 = total.sum(axis=1, keepdims=True)
	#normalized1 = np.where(normalized1!=0,total/normalized1,0.)
	#own_assoc1 = np.where(voc._content!=0,normalized1,0.)
	#others1 = normalized1-own_assoc1

	#entr1 = scipy.special.entr(own_assoc1).sum()# + scipy.special.entr(others1.sum(axis=0)).sum()

	return entr0 + entr1




#def new_entropy_withvoc_max(pop):
#	return 1

def new_entropy_withvoc_min(pop):
	return 0

FUNC=new_entropy_withvoc
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":new_entropy_withvoc_min}#,"ymax":new_entropy_withvoc_max}
custom_new_entropy_withvoc=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["success_mw"],**graphconfig)


#########new_entropy_globalnorm##########

def new_entropy_globalnorm(agent=None,mem=None,voc=None,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary

	success = mem['success_mw']

	norms = success.sum()#keepdims=True)
	if not (norms.all() == 0):
		normalized = success/norms
	else:
		normalized = success
	entr = scipy.special.entr(normalized).sum()

	return entr




#def new_entropy_globalnorm_max(pop):
#	return 1

def new_entropy_globalnorm_min(pop):
	return 0

FUNC=new_entropy_globalnorm
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":new_entropy_globalnorm_min}#,"ymax":new_entropy_globalnorm_max}
custom_new_entropy_globalnorm=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["success_mw"],**graphconfig)


#########new_entropy_success_rate##########

def new_entropy_success_rate(agent=None,mem=None,voc=None,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary

	success = mem['success_mw']
	failure = mem['success_mw']
	total = success + failure

	success_rate = np.where(total!=0,success/total,0.)

	normalized0 = success_rate.sum(axis=0, keepdims=True)
	normalized0 = np.where(normalized0!=0,success_rate/normalized0,0.)
	entr0 = scipy.special.entr(normalized0).sum()#.sum(axis=0)

	normalized1 = success_rate.sum(axis=1, keepdims=True)
	normalized1 = np.where(normalized1!=0,success_rate/normalized1,0.)
	entr1 = scipy.special.entr(normalized1).sum()#.sum(axis=1)

	return entr0 + entr1




#def new_entropy_success_rate_max(pop):
#	return 1

def new_entropy_success_rate_min(pop):
	return 0

FUNC=new_entropy_success_rate
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":new_entropy_success_rate_min}#,"ymax":new_entropy_success_rate_max}
custom_new_entropy_success_rate=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["success_mw"],**graphconfig)


#########transinformation##########

def voc_transinf(voc):
	M = voc.get_M()
	W = voc.get_W()
	KM = voc.get_known_meanings()
	Mtransinf = len(KM)*np.log2(W)
	for m in KM:
		Mtransinf -= np.log2(len(voc.get_known_words(m=m)))
	return Mtransinf*1./M

def transinformation(agent,**kwargs):
	voc = agent._vocabulary
	return voc_transinf(voc)

def transinformation_max(pop):
	return np.log2(pop.get_W())

def transinformation_min(pop):
	return 0

FUNC=transinformation
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":transinformation_min,"ymax":transinformation_max}
custom_transinformation=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########connex_components_per_word##########CAT

def connex_components_per_word(agent,**kwargs):
	if agent._vocabulary._content_decoding:
		return sum([len(x) for x in list(agent._vocabulary._content_decoding.values())])/float(len(list(agent._vocabulary._content_decoding.keys())))
	else:
		return 0

def connex_components_per_word_max(pop):
	return 1

def connex_components_per_word_min(pop):
	return 0

FUNC=connex_components_per_word
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":connex_components_per_word_min}#,"ymax":connex_components_per_word_max}
custom_connex_components_per_word=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)

#########Ncat_percept##########CAT

def Ncat_percept(agent,**kwargs):
	return len(agent._vocabulary._content_coding)

def Ncat_percept_max(pop):
	return 1

def Ncat_percept_min(pop):
	return 0

FUNC=Ncat_percept
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Ncat_percept_min}#,"ymax":Ncat_percept_max}
custom_Ncat_percept=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)

#########Ncat_semantic##########CAT

def Ncat_semantic(agent,**kwargs):
	n = 0
	data = None
	for iv in sorted(agent._vocabulary._content_coding):
		val = max([0]+list(iv.data.values()))
		data1 = [w for w,v in list(iv.data.items()) if v == val]
		if data != data1:
			data = copy.copy(data1)
			n += 1
	return n

def Ncat_semantic_max(pop):
	return 1

def Ncat_semantic_min(pop):
	return 0

FUNC=Ncat_semantic
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Ncat_semantic_min}#,"ymax":Ncat_semantic_max}
custom_Ncat_semantic=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)


#########N_words##########

def N_words(agent,**kwargs):
	if hasattr(agent._vocabulary,'_content_decoding'):
		return len(list(agent._vocabulary._content_decoding.keys()))
	else:
		return len(agent._vocabulary.get_known_words())

def N_words_max(pop):
	if hasattr(pop.env,'W'):
		return pop.env.W
	elif hasattr(pop._agentlist[0]._vocabulary,'get_W'):
		return pop._agentlist[0]._vocabulary.get_W()
	else:
		return None

def N_words_min(pop):
	return 0

FUNC=N_words
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_words_min,"ymax":N_words_max}
custom_N_words=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_meanings##########

def N_meanings(agent,**kwargs):
	return len(agent._vocabulary.get_known_meanings())

def N_meanings_max(pop):
	if hasattr(pop.env,'M'):
		return pop.env.M
	elif hasattr(pop._agentlist[0]._vocabulary,'get_M'):
		return pop._agentlist[0]._vocabulary.get_M()
	else:
		return None

def N_meanings_min(pop):
	return 0

FUNC=N_meanings
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_meanings_min,"ymax":N_meanings_max}
custom_N_meanings=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_w_per_m##########

def N_w_per_m(agent,**kwargs):
	if not agent._vocabulary.get_known_meanings():
		return 0
	else:
		return float(Nlink(agent))/len(agent._vocabulary.get_known_meanings())

def N_w_per_m_max(pop):
	return 1

def N_w_per_m_min(pop):
	return 0

FUNC=N_w_per_m
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_w_per_m_min}#,"ymax":N_w_per_m_max}
custom_N_w_per_m=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_w_per_m_agentmax##########

def N_w_per_m_agentmax(agent,**kwargs):
	if not agent._vocabulary.get_known_meanings():
		return 0
	else:
		return max([len(agent._vocabulary.get_known_words(m=m)) for m in agent._vocabulary.get_known_meanings()])

def N_w_per_m_agentmax_max(pop):
	return 1

def N_w_per_m_agentmax_min(pop):
	return 0

FUNC=N_w_per_m_agentmax
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_w_per_m_agentmax_min}#,"ymax":N_w_per_m_max}
custom_N_w_per_m_agentmax=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)
#########N_m_per_w##########

def N_m_per_w(agent,**kwargs):
	if not agent._vocabulary.get_known_words():
		return 0
	else:
		return float(Nlink(agent))/len(agent._vocabulary.get_known_words())

def N_m_per_w_max(pop):
	return 1

def N_m_per_w_min(pop):
	return 0

FUNC=N_m_per_w
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_m_per_w_min}#,"ymax":N_m_per_w_max}
custom_N_m_per_w=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_m_per_w_agentmax##########

def N_m_per_w_agentmax(agent,**kwargs):
	if not agent._vocabulary.get_known_words():
		return 0
	else:
		return max([len(agent._vocabulary.get_known_meanings(w=w)) for w in agent._vocabulary.get_known_words()])

def N_m_per_w_agentmax_max(pop):
	return 1

def N_m_per_w_agentmax_min(pop):
	return 0

FUNC=N_m_per_w_agentmax
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_m_per_w_agentmax_min}#,"ymax":N_m_per_w_max}
custom_N_m_per_w_agentmax=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########homonymy_simple##########

def homonymy_simple(agent,**kwargs):
	return Nlink(agent)-N_meanings(agent)

def homonymy_simple_max(pop):
	return 1

def homonymy_simple_min(pop):
	return 0

FUNC=homonymy_simple
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":homonymy_simple_min}#,"ymax":N_m_per_w_max}
custom_homonymy_simple=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########homonymy##########

def homonymy(agent,**kwargs):
	return sum([ scipy.special.binom(len(agent._vocabulary.get_known_meanings(w=w)),2) for w in agent._vocabulary.get_known_words()])

def homonymy_max(pop):
	return 1

def homonymy_min(pop):
	return 0

FUNC=homonymy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":homonymy_min}#,"ymax":N_m_per_w_max}
custom_homonymy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########synonymy_simple##########

def synonymy_simple(agent,**kwargs):
	return Nlink(agent)-N_words(agent)

def synonymy_simple_max(pop):
	return 1

def synonymy_simple_min(pop):
	return 0

FUNC=synonymy_simple
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":synonymy_simple_min}#,"ymax":N_m_per_w_max}
custom_synonymy_simple=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########synonymy##########

def synonymy(agent,**kwargs):
	return sum([ scipy.special.binom(len(agent._vocabulary.get_known_words(m=m)),2) for m in agent._vocabulary.get_known_meanings()])

def synonymy_max(pop):
	return 1

def synonymy_min(pop):
	return 0

FUNC=synonymy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":synonymy_min}#,"ymax":N_m_per_w_max}
custom_synonymy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########cat_synonymy##########CAT

def cat_synonymy(agent,**kwargs):
	n = 0
	w = 0
	for iv in sorted(agent._vocabulary._content_coding):
		w += len(iv.data)
		n += 1
	return w / float(n)

def cat_synonymy_max(pop):
	return 1

def cat_synonymy_min(pop):
	return 0

FUNC=cat_synonymy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":cat_synonymy_min}#,"ymax":cat_synonymy_max}
custom_cat_synonymy=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)


#########norm_std_Ncat##########CAT

def norm_std_Ncat(agent,**kwargs):
	ncat = Ncat_semantic(agent)
	cat_l = agent._vocabulary.get_known_meanings()
	var = sum([(len(cat)-1./ncat)**2 for cat in cat_l])/float(ncat)
	return ncat*np.sqrt(var)

def norm_std_Ncat_max(pop):
	return 1

def norm_std_Ncat_min(pop):
	return 0

FUNC=norm_std_Ncat
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":norm_std_Ncat_min}#,"ymax":norm_std_Ncat_max}
custom_norm_std_Ncat=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)


#########norm_std_Npercept##########CAT

def norm_std_Npercept(agent,**kwargs):
	ncat = Ncat_percept(agent)
	cat_l = agent._vocabulary._content_coding
	var = sum([(len(cat)-1./ncat)**2 for cat in cat_l])/float(ncat)
	return ncat*np.sqrt(var)

def norm_std_Npercept_max(pop):
	return 1

def norm_std_Npercept_min(pop):
	return 0

FUNC=norm_std_Npercept
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":norm_std_Npercept_min}#,"ymax":norm_std_Npercept_max}
custom_norm_std_Npercept=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)


#########dist_threshold##########CAT

def dist_threshold(agent,**kwargs):
	if hasattr(agent._strategy,'get_dist_threshold'):
		return agent._strategy.get_dist_threshold(agent._vocabulary,agent._memory)
	else:
		return 0

def dist_threshold_max(pop):
	return 1

def dist_threshold_min(pop):
	return 0

FUNC=dist_threshold
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":dist_threshold_min,"ymax":dist_threshold_max}
custom_dist_threshold=custom_func.CustomFunc(FUNC_BIS,"agent",tags='category',**graphconfig)

#########N_accessible_meanings##########

def N_accessible_meanings(agent,**kwargs):
	return agent._vocabulary.get_M()

def N_accessible_meanings_min(pop):
	return 0

FUNC=N_accessible_meanings
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_accessible_meanings_min}#,"ymax":N_accessible_meanings_max}
custom_N_accessible_meanings=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_unknown_meanings##########

def N_unknown_meanings(agent,**kwargs):
	return len(agent._vocabulary.get_unknown_meanings())

def N_unknown_meanings_min(pop):
	return 0

FUNC=N_unknown_meanings
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_unknown_meanings_min}#,"ymax":N_unknown_meanings_max}
custom_N_unknown_meanings=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_unknown_words##########

def N_unknown_words(agent,**kwargs):
	return len(agent._vocabulary.get_unknown_words())

def N_unknown_words_min(pop):
	return 0

FUNC=N_unknown_words
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_unknown_words_min}#,"ymax":N_unknown_words_max}
custom_N_unknown_words=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_accessible_words##########

def N_accessible_words(agent,**kwargs):
	return agent._vocabulary.get_W()

def N_accessible_words_min(pop):
	return 0

FUNC=N_accessible_words
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_accessible_words_min}#,"ymax":N_accessible_words_max}
custom_N_accessible_words=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########N_exploring_words##########

def N_exploring_words(agent,**kwargs):
	ans = 0.
	for w in agent._vocabulary.get_known_words():
		if 0 < srtheo_local(agent=agent,w=w) < 1:
			ans += 1.
	return ans

def N_exploring_words_min(pop):
	return 0

FUNC=N_exploring_words
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_exploring_words_min}#,"ymax":N_accessible_words_max}
custom_N_exploring_words=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########N_exploring_meanings##########

def N_exploring_meanings(agent,**kwargs):
	ans = 0.
	for m in agent._vocabulary.get_known_meanings():
		if srtheo_local(agent=agent,m=m) < 1.:
			ans += 1.
	return ans

def N_exploring_meanings_min(pop):
	return 0

FUNC=N_exploring_meanings
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_exploring_meanings_min}#,"ymax":N_accessible_meanings_max}
custom_N_exploring_meanings=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)
#########time_before_explo##########

def time_since_explo(agent,**kwargs):
	if 'time_since_explo' in list(agent._memory.keys()):
		return agent._memory['time_since_explo']
	else:
		return 0

def time_since_explo_min(pop):
	return 0

FUNC=time_since_explo
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":time_since_explo_min}#,"ymax":time_since_explo_max}
custom_time_since_explo=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########srtheo_local##########

def srtheo_local(agent, m=None, w=None, **kwargs):
	ag = agent
	if 'interact_count_m' in list(ag._memory.keys()) or 'interact_count_voc' in list(ag._memory.keys()):
	#if 'interact_count_m' in pop._agentlist[0]._memory.keys() or 'interact_count_voc' in pop._agentlist[0]._memory.keys():
		#for ag in pop._agentlist:
		if hasattr(ag._vocabulary,'_content'):
			return srtheo_utils.srtheo_voc(ag._vocabulary._content, m=m, w=w, voc2_m=ag._memory['interact_count_m'],voc2_w=ag._memory['interact_count_w'])
		else:
			return srtheo_utils.srtheo_voc(ag._vocabulary, m=m, w=w, voc2=ag._memory['interact_count_voc'])
	else:
		return 0

def srtheo_local_min(pop):
	return 0

def srtheo_local_max(pop):
	return 1.


FUNC = srtheo_local
FUNC_BIS=pop_ize(FUNC)
graphconfig = {"ymin":srtheo_local_min,"ymax":srtheo_local_max}
custom_srtheo_local = custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########entropy##########

def tempentropy(MM,WW):
	a=0
	for i in range(int(WW-MM+1),int(WW+1)):
		a+=np.log2(i)
	return a

def entropy(agent,**kwargs):
	m=len(agent._vocabulary.get_known_meanings())
	return tempentropy(agent._vocabulary.get_M()-m,agent._vocabulary.get_W()-m)

def entropy_max(pop):
	return tempentropy(pop.get_M(),pop.get_W())

def entropy_min(pop):
	return 0

FUNC=entropy
FUNC_BIS=pop_ize(FUNC)
entropy_moyen=pop_ize(FUNC)
graphconfig={"ymin":entropy_min,"ymax":entropy_max}
custom_entropy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########entropy_moyen_norm##########


def entropy_moyen_norm(pop,**kwargs):
	return 1.-(entropy_moyen(pop)[0]/entropy_max(pop))

def entropy_moyen_norm_max(pop):
	return 1

def entropy_moyen_norm_min(pop):
	return 0

FUNC=entropy_moyen_norm
graphconfig={"ymin":entropy_moyen_norm_min,"ymax":entropy_moyen_norm_max}
custom_entropy_moyen_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########zipf_exponent_m##########

def zipf_exponent_m(agent, **kwargs):
	return zipf_utils.zipf_current(agent=agent,option='m')[0]

def zipf_exponent_min(pop):
	return 0



FUNC = zipf_exponent_m
FUNC_BIS=pop_ize(FUNC)
graphconfig = {"ymin":zipf_exponent_min}
custom_zipf_exponent_m = custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########zipf_error_m##########

def zipf_error_m(agent, **kwargs):
	return zipf_utils.zipf_current(agent=agent,option='m')[1]

def zipf_error_min(pop):
	return 0

def zipf_error_max(pop):
	return 1.


FUNC = zipf_error_m
FUNC_BIS=pop_ize(FUNC)
graphconfig = {"ymin":zipf_error_min,"ymax":zipf_error_max}
custom_zipf_error_m = custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########zipf_exponent_w##########

def zipf_exponent_w(agent, **kwargs):
	return zipf_utils.zipf_current(agent=agent,option='w')[0]

FUNC = zipf_exponent_w
FUNC_BIS=pop_ize(FUNC)
graphconfig = {"ymin":zipf_exponent_min}
custom_zipf_exponent_w = custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########zipf_error_w##########

def zipf_error_w(agent, **kwargs):
	return zipf_utils.zipf_current(agent=agent,option='w')[1]


FUNC = zipf_error_w
FUNC_BIS=pop_ize(FUNC)
graphconfig = {"ymin":zipf_error_min,"ymax":zipf_error_max}
custom_zipf_error_w = custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########optimalvocpolicy##########

def optimalvocpolicy(agent,**kwargs):
	v = agent._memory['interact_count_voc']
	v2 = v.empty_copy()
	for m in v.get_known_meanings():
		w = v.get_known_words(m=m,option='max')[0]
		v2.add(m=m,w=w,content_type='m')
	for w in v.get_known_words():
		m = v.get_known_meanings(w=w,option='max')[0]
		v2.add(m=m,w=w,content_type='w')
	return srtheo_utils.srtheo_voc(voc1=v,voc2=v2)

def optimalvocpolicy_max(pop):
	return 1.

def optimalvocpolicy_min(pop):
	return 0

FUNC=optimalvocpolicy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":optimalvocpolicy_min,"ymax":optimalvocpolicy_max}
custom_optimalvocpolicy=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["interact_count_voc"],**graphconfig)

#########nb_inventions_per_known_m_per_agent##########

def nb_inventions_per_known_m_per_agent(agent,**kwargs):
	KM = len(agent._vocabulary.get_known_meanings())
	if KM:
		return agent._memory['inventions']['nb_inventions']*1./KM
	else:
		return 0

def nb_inventions_per_known_m_per_agent_max(pop):
	return 1.

def nb_inventions_per_known_m_per_agent_min(pop):
	return 0

FUNC=nb_inventions_per_known_m_per_agent
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":nb_inventions_per_known_m_per_agent_min}#,"ymax":nb_inventions_per_known_m_per_agent_max}
custom_nb_inventions_per_known_m_per_agent=custom_func.CustomFunc(FUNC_BIS,"agent",tags=["interact_count_voc"],**graphconfig)

############################	LEVEL MEANING ############################

####	INPUT:		meaning, pop , **progress_info
####	OUTPUT:		[mean,std,(tempNlist)]

#	FUNC_BIS=meaning_pop_ize(FUNC)
#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"meaning",**graphconfig)

#########agent_usage##########

def agent_usage(m,pop,**kwargs):
	return len([ 0 for ag in pop._agentlist if m in ag._vocabulary.get_known_meanings()])


def agent_usage_max(pop):
	return pop.get_M() * pop.get_W()

def agent_usage_min(pop):
	return 0


FUNC = agent_usage
FUNC_BIS = meaning_pop_ize(FUNC)
graphconfig = {"ymin":agent_usage_min}#,"ymax":agent_usage_max}
custom_agent_usage = custom_func.CustomFunc(FUNC_BIS,"meaning",**graphconfig)

#########nb_inventions_per_m##########

def nb_inventions_per_m(m,pop,**kwargs):
	return sum([ len(ag._memory['inventions']['invented_meanings'][m]) for ag in pop._agentlist if m in list(ag._memory['inventions']['invented_meanings'].keys())])

def nb_inventions_per_m_max(pop):
	return pop.get_M() * pop.get_W()

def nb_inventions_per_m_min(pop):
	return 0


FUNC = nb_inventions_per_m
FUNC_BIS = meaning_pop_ize(FUNC)
graphconfig = {"ymin":nb_inventions_per_m_min}#,"ymax":nb_inventions_per_m_max}
custom_nb_inventions_per_m = custom_func.CustomFunc(FUNC_BIS,"meaning",**graphconfig)

#########nb_interactions_per_m##########

def nb_interactions_per_m(m,pop,**kwargs):
	return sum([ag._memory['inventions']['counts'][m]  for ag in pop._agentlist if m in list(ag._memory['inventions']['counts'].keys())])

def nb_interactions_per_m_max(pop):
	return pop.get_M() * pop.get_W()

def nb_interactions_per_m_min(pop):
	return 0


FUNC = nb_interactions_per_m
FUNC_BIS = meaning_pop_ize(FUNC)
graphconfig = {"ymin":nb_interactions_per_m_min}#,"ymax":nb_interactions_per_m_max}
custom_nb_interactions_per_m = custom_func.CustomFunc(FUNC_BIS,"meaning",**graphconfig)

############################	LEVEL POPULATION ############################

#### 	INPUT:		pop, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_d##########

def N_d(pop,**kwargs):
	if hasattr(pop._agentlist[0]._vocabulary,'_content'):
		tempmat = np.matrix(np.zeros((pop.get_M(),pop.get_W())))
		for agent in pop._agentlist:
			tempmat += agent._vocabulary._content
		tempmat[tempmat>0] = 1
		return np.sum(tempmat)
	else:
		d_set = []
		for ag in pop._agentlist:
			for m in ag._vocabulary.get_known_meanings():
				for w in ag._vocabulary.get_known_words(m=m):
					if (m,w) not in d_set:
						d_set.append((m,w))
		return len(d_set)

def N_d_max(pop):
	return pop.get_M()*pop.get_W()

def N_d_min(pop):
	return 0

FUNC=N_d
graphconfig={"ymin":N_d_min}#,"ymax":N_d_max}
custom_N_d=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_d_m##########

def N_d_m(pop,**kwargs):
	if hasattr(pop._agentlist[0]._vocabulary,'_content'):
		tempmat = np.matrix(np.zeros((pop.get_M(),pop.get_W())))
		for agent in pop._agentlist:
			tempmat += agent._vocabulary._content
		tempmat[tempmat>0] = 1
		return np.sum(tempmat[0,:])
	else:
		d_set = []
		for ag in pop._agentlist:
			if ag._vocabulary.get_known_meanings():
				m = ag._vocabulary.get_known_meanings()[0]
				for w in ag._vocabulary.get_known_words(m=m):
					if (m,w) not in d_set:
						d_set.append((m,w))
		return len(d_set)


def N_d_m_max(pop):
	return pop.get_W()

def N_d_m_min(pop):
	return 0

FUNC=N_d_m
graphconfig={"ymin":N_d_m_min}#,"ymax":N_d_m_max}
custom_N_d_m=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_d_m_ag##########

def N_d_m_ag(pop,**kwargs):
	if hasattr(pop._agentlist[0]._vocabulary,'_content'):
		tempmat = np.matrix(np.zeros((pop.get_M(),pop.get_W())))
		agent = pop._agentlist[0]
		tempmat += agent._vocabulary._content
		tempmat[tempmat>0] = 1
		return np.sum(tempmat[0,:])
	else:
		d_set = []
		ag = pop._agentlist[0]
		if ag._vocabulary.get_known_meanings():
			m = ag._vocabulary.get_known_meanings()[0]
			for w in ag._vocabulary.get_known_words(m=m):
				if (m,w) not in d_set:
					d_set.append((m,w))
		return len(d_set)

def N_d_m_ag_max(pop):
	return pop.get_W()

def N_d_m_ag_min(pop):
	return 0

FUNC=N_d_m_ag
graphconfig={"ymin":N_d_m_ag_min}#,"ymax":N_d_m_ag_max}
custom_N_d_m_ag=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs##########

def Nlinksurs(pop,**kwargs):
	if hasattr(pop._agentlist[0]._vocabulary,'_content'):
		tempmat=np.matrix(np.ones((pop.get_M(),pop.get_W())))
		for agent in pop._agentlist:
			tempmat=np.multiply(tempmat,agent._vocabulary.get_content())
			tempmat[tempmat>0] = 1
		return np.sum(tempmat)
	else:
		d_set = []
		ag = pop._agentlist[0]
		for m in ag._vocabulary.get_known_meanings():
			for w in ag._vocabulary.get_known_words(m=m):
				if (m,w) not in d_set:
					d_set.append((m,w))
		for ag in pop._agentlist:
			for (m,w) in [(m1,w1) for (m1,w1) in d_set]:#list comprehension because d_set modified on the fly
				if m not in ag._vocabulary.get_known_meanings() or w not in ag._vocabulary.get_known_words(m=m):
					d_set.remove((m,w))
		return len(d_set)

def Nlinksurs_max(pop):
	return pop.get_M()

def Nlinksurs_min(pop):
	return 0

FUNC=Nlinksurs
graphconfig={"ymin":Nlinksurs_min,"ymax":Nlinksurs_max}
custom_Nlinksurs=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs_couples##########

def Nlinksurs_couples(pop,**kwargs):
	tempvalues = []
	if hasattr(pop._agentlist[0]._vocabulary,'_content'):
		for j in range(100):
			agent1_id=pop.pick_speaker()
			agent2_id=pop.pick_hearer(agent1_id)
			agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
			agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
			tempm = np.linalg.matrix_rank(np.multiply(agent1.get_vocabulary_content(),agent2.get_vocabulary_content()))
			tempvalues.append(tempm)
		return np.mean(tempvalues)
	else:
		for j in range(100):
			d_set = []
			agent1_id=pop.pick_speaker()
			agent2_id=pop.pick_hearer(agent1_id)
			agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
			agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
			for m in agent1._vocabulary.get_known_meanings():
				for w in agent1._vocabulary.get_known_words(m=m):
					if (m,w) not in d_set:
						d_set.append((m,w))
			for (m,w) in [(m1,w1) for (m1,w1) in d_set]:#list comprehension because d_set modified on the fly
				if m not in agent2._vocabulary.get_known_meanings() or w not in agent2._vocabulary.get_known_words(m=m):
					d_set.remove((m,w))
			tempvalues.append(len(d_set))
		return np.mean(tempvalues)


def Nlinksurs_couples_max(pop):
	return pop.get_M()

def Nlinksurs_couples_min(pop):
	return 0

FUNC=Nlinksurs_couples
graphconfig={"ymin":Nlinksurs_couples_min,"ymax":Nlinksurs_couples_max}
custom_Nlinksurs_couples=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########optimalvocpolicy_pop##########

def optimalvocpolicy_pop(pop,**kwargs):
	v = pop.get_average_voc()
	v2 = v.empty_copy()
	for m in v.get_known_meanings():
		w = v.get_known_words(m=m,option='max')[0]
		v2.add(m=m,w=w,content_type='m')
	for w in v.get_known_words():
		m = v.get_known_meanings(w=w,option='max')[0]
		v2.add(m=m,w=w,content_type='w')
	return srtheo_utils.srtheo_voc(voc1=v,voc2=v2)

def optimalvocpolicy_pop_max(pop):
	return 1.

def optimalvocpolicy_pop_min(pop):
	return 0

FUNC=optimalvocpolicy_pop
graphconfig={"ymin":optimalvocpolicy_pop_min,"ymax":optimalvocpolicy_pop_max}
custom_optimalvocpolicy_pop=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropypop##########

def entropypop(pop,**kwargs):
	m=Nlinksurs(pop)
	return tempentropy(pop.get_M()-m,pop.get_W()-m)

def entropypop_max(pop):
	return tempentropy(pop.get_M(),pop.get_W())

def entropypop_min(pop):
	return 0

FUNC=entropypop
graphconfig={"ymin":entropypop_min,"ymax":entropypop_max}
custom_entropypop=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropypopnorm##########


def entropypop_norm(pop,**kwargs):
	return 1-(entropypop(pop)/entropypop_max(pop))

def entropypop_norm_max(pop):
	return 1

def entropypop_norm_min(pop):
	return 0

FUNC=entropypop_norm
graphconfig={"ymin":entropypop_norm_min,"ymax":entropypop_norm_max}
custom_entropypop_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)


#########entropycouplesold##########

def entropycouples_old(pop,**kwargs):
	if not hasattr(pop._agentlist[0]._vocabulary,'_content'):
		raise ValueError('this measure is not implemented for this type of vocabulary')
	tempvalues=[]
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		if pop._strat_cfg["strat_type"][-5:]=="_real":
			voc1=agent1._vocabulary.get_content()
			voc2=agent2._vocabulary.get_content()
			tempm=0
			for m in range(pop.get_M()):
				for w in range(pop.get_W()):
					test1= voc1[m,w] and voc2[m,w]
					test1=test1 and agent1._vocabulary.get_known_meanings(w)==[m]
					test1=test1 and agent2._vocabulary.get_known_meanings(w)==[m]
					test1=test1 and agent1._vocabulary.get_known_words(m)==[w]
					test1=test1 and agent2._vocabulary.get_known_words(m)==[w]
					if test1:
						tempm+=1
		else:
			tempmat=np.multiply(agent1._vocabulary.get_content(),agent2._vocabulary.get_content())
			tempm=np.sum(tempmat)
		tempvalues.append(tempentropy(pop.get_M()-tempm,pop.get_W()-tempm))
	return np.mean(tempvalues)

def entropycouples_old_max(pop):
	return tempentropy(pop.get_M(),pop.get_W())

def entropycouples_old_min(pop):
	return 0

FUNC=entropycouples_old
graphconfig={"ymin":entropycouples_old_min,"ymax":entropycouples_old_max}
custom_entropycouples_old=custom_func.CustomFunc(FUNC,"population",tags=["old_voc"],**graphconfig)

#########entropycouplesoldnorm##########


def entropycouples_old_norm(pop,**kwargs):
	return 1-(entropycouples(pop)/entropycouples_max(pop))

def entropycouples_old_norm_max(pop):
	return 1

def entropycouples_old_norm_min(pop):
	return 0

FUNC=entropycouples_old_norm
graphconfig={"ymin":entropycouples_old_norm_min,"ymax":entropycouples_old_norm_max}
custom_entropycouples_old_norm=custom_func.CustomFunc(FUNC,"population",tags=["old_voc"],**graphconfig)

#########explo_rate##########


def explo_rate(pop,**kwargs):
	count = 0.
	for hist in pop._past:
		if hist[6]:
			count += 1.
	if len(pop._past) == 0:
		return 1.
	else:
		return count/len(pop._past)

def explo_rate_max(pop):
	return 1.

def explo_rate_min(pop):
	return 0.

FUNC=explo_rate
graphconfig={"ymin":explo_rate_min,"ymax":explo_rate_max}
custom_explo_rate=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########relative_explo_rate##########


def relative_explo_rate(pop,**kwargs):
	Nm = pop_ize(N_meanings)(pop,**kwargs)[0]
	naive_explo = 1.-(float(Nm)/N_meanings_max(pop,**kwargs))
	if naive_explo == 0.:
		return 1.
	else:
		return explo_rate(pop,**kwargs)/naive_explo

def relative_explo_rate_min(pop):
	return 0

FUNC=relative_explo_rate
graphconfig={"ymin":relative_explo_rate_min}#,"ymax":relative_explo_rate_max}
custom_relative_explo_rate=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_words_pop##########CAT


def N_words_pop(pop,**kwargs):
	words = set()
	for ag in pop._agentlist:
		for w in list(ag._vocabulary._content_decoding.keys()):
			words.add(w)
	return len(words)

def N_words_pop_max(pop):
	return 1

def N_words_pop_min(pop):
	return 0

FUNC=N_words_pop
graphconfig={"ymin":N_words_pop_min}#,"ymax":entropycouples_old_norm_max}
custom_N_words_pop=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

#########N_words_ratio##########CAT


def N_words_ratio(pop,**kwargs):
	words = set()
	n = 0
	for ag in pop._agentlist:
		for w in list(ag._vocabulary._content_decoding.keys()):
			words.add(w)
			n += 1
	if n:
		return len(words)*len(pop._agentlist)/float(n)
	else:
		return 0

def N_words_ratio_max(pop):
	return 1

def N_words_ratio_min(pop):
	return 0

FUNC=N_words_ratio
graphconfig={"ymin":N_words_ratio_min}#,"ymax":entropycouples_old_norm_max}
custom_N_words_ratio=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

#########distance_used##########CAT


def distance_used(pop,**kwargs):
	if pop._lastgameinfo:
		return abs(pop._lastgameinfo[-1][0]-pop._lastgameinfo[-1][1])
	else:
		return 1

def distance_used_max(pop):
	return 1

def distance_used_min(pop):
	return 0

FUNC=distance_used
graphconfig={"ymin":distance_used_min,"ymax":entropycouples_old_norm_max}
custom_distance_used=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)


#########discrim_success##########CAT

def discrim_success(pop,**kwargs):
	n = 0
	for i in range(100):
		agent = random.choice(pop._agentlist)
		m1, m2 = next(agent._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2))
		if agent._vocabulary.get_category(m1) != agent._vocabulary.get_category(m2):
			n += 1
		agent._vocabulary.del_cache()
	return n/100.

def discrim_success_max(pop):
	return 1

def discrim_success_min(pop):
	return 0

FUNC=discrim_success
graphconfig={"ymin":discrim_success_min,"ymax":discrim_success_max}
custom_discrim_success=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

#########discrim_success_semantic##########CAT

def discrim_success_semantic(pop,**kwargs):
	n = 0
	for i in range(100):
		agent = random.choice(pop._agentlist)
		m1, m2 = next(agent._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2))
		wl_1 = agent._vocabulary.get_known_words(m1,option='max')
		wl_2 = agent._vocabulary.get_known_words(m2,option='max')
		if wl_1 != wl_2:
			n += 1

		agent._vocabulary.del_cache()
	return n/100.

def discrim_success_semantic_max(pop):
	return 1

def discrim_success_semantic_min(pop):
	return 0

FUNC=discrim_success_semantic
graphconfig={"ymin":discrim_success_semantic_min,"ymax":discrim_success_semantic_max}
custom_discrim_success_semantic=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)


#########actual_successrate##########


def actual_successrate(pop,**kwargs):
	s = 0
	f = 0
	for info in pop._past:
		if info[3]:
			s += 1
		else:
			f += 1
	if not s:
		return 0
	else:
		return s/float(s+f)

def actual_successrate_max(pop):
	return 1

def actual_successrate_min(pop):
	return 0

FUNC=actual_successrate
graphconfig={"ymin":actual_successrate_min,"ymax":actual_successrate_max}
custom_actual_successrate=custom_func.CustomFunc(FUNC,"population",**graphconfig)


#########entropycouples##########

def entropycouples(pop,**kwargs):
	if not hasattr(pop._agentlist[0]._vocabulary,'_content'):
		raise ValueError('this measure is not implemented for this type of vocabulary')
	tempvalues=[]
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		tempm = np.linalg.matrix_rank(np.multiply(agent1.get_vocabulary_content(),agent2.get_vocabulary_content()))
		tempvalues.append(tempentropy(pop.get_M()-tempm,pop.get_W()-tempm))
	return np.mean(tempvalues)

def entropycouples_max(pop):
	return tempentropy(pop.get_M(),pop.get_W())

def entropycouples_min(pop):
	return 0

FUNC=entropycouples
graphconfig={"ymin":entropycouples_min,"ymax":entropycouples_max}
custom_entropycouples=custom_func.CustomFunc(FUNC,"population",tags=["old_voc"],**graphconfig)

#########entropycouplesnorm##########


def entropycouples_norm(pop,**kwargs):
	return 1-(entropycouples(pop)/entropycouples_max(pop))

def entropycouples_norm_max(pop):
	return 1

def entropycouples_norm_min(pop):
	return 0

FUNC=entropycouples_norm
graphconfig={"ymin":entropycouples_norm_min,"ymax":entropycouples_norm_max}
custom_entropycouples_norm=custom_func.CustomFunc(FUNC,"population",tags=["old_voc"],**graphconfig)

#########exec_time##########


def exec_time(pop,**kwargs):
	if hasattr(pop,'_exec_time'):
		return pop._exec_time
	else:
		return 0

def exec_time_min(pop):
	return 0

FUNC=exec_time
graphconfig={"ymin":exec_time_min}
custom_exec_time=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########cat_agreement##########CAT

def cat_agreement(pop,**kwargs):
	agr = 0
	for i in range(100):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		agent1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		#ivt1 = copy.deepcopy(agent1._vocabulary._content_decoding)
		#ivt2 = copy.deepcopy(agent2._vocabulary._content_decoding)

		ivt1 = {}
		ivt2 = {}

		for iv in agent1._vocabulary._content_coding:
			val_max = max([0]+list(iv.data.values()))
			wl = [w for w,v in list(iv.data.items()) if v == val_max]
			if wl:
				ivt1.setdefault(wl[0], IntervalTree()).add(Interval(iv.begin,iv.end))
		for iv in agent2._vocabulary._content_coding:
			val_max = max([0]+list(iv.data.values()))
			wl = [w for w,v in list(iv.data.items()) if v == val_max]
			if wl:
				ivt2.setdefault(wl[0], IntervalTree()).add(Interval(iv.begin,iv.end))

		for w in list(ivt1.keys()):
			ivt1[w].merge_overlaps()
		for w in list(ivt2.keys()):
			ivt2[w].merge_overlaps()

		ivt = IntervalTree()
		for w in list(ivt1.keys()):
			if w in list(ivt2.keys()):
				for iv in ivt1[w]:
					ivt2[w].slice(iv.end)
					ivt2[w].slice(iv.begin)
				for iv in ivt2[w]:
					ivt1[w].slice(iv.end)
					ivt1[w].slice(iv.begin)
				ivt.update(ivt1[w] & ivt2[w])
		ivt.merge_overlaps()
		agr += sum([iv.end-iv.begin for iv in ivt])
	return agr/100.

def cat_agreement_max(pop):
	return 1

def cat_agreement_min(pop):
	return 0

FUNC=cat_agreement
graphconfig={"ymin":cat_agreement_min,"ymax":cat_agreement_max}
custom_cat_agreement=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

#########srtheo##########

def srtheo(pop, m=None, **kwargs):
	fail=0
	succ=0
	for i in range(100):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		agent1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		if m is None:
			ms = agent1._vocabulary.get_random_m()
		else:
			ms = m
		w = agent1._vocabulary.get_random_known_w(m=ms)
		mh = agent2._vocabulary.get_random_known_m(w=w)
		if agent2.eval_success(ms=ms, w=w, mh=mh):
			succ += 1
		else:
			fail += 1
		agent1._vocabulary.del_cache()
		agent2._vocabulary.del_cache()
	return succ/float(succ+fail)

def srtheo_max(pop):
	return 1

def srtheo_min(pop):
	return 0

FUNC=srtheo
graphconfig={"ymin":srtheo_min,"ymax":srtheo_max}
custom_srtheo=custom_func.CustomFunc(FUNC,"population",**graphconfig)
#########decay_coherence##########

def decay_coherence(pop, m=None, **kwargs):
	if not hasattr(pop.agent_init,'converged_voc'):
		return 0
	else:
		v1 = pop.agent_init.converged_voc
		v2 = pop.get_average_voc()
		return srtheo_utils.srtheo_voc(voc1=v1,voc2=v2)


def decay_coherence_max(pop):
	return 1

def decay_coherence_min(pop):
	return 0

FUNC=decay_coherence
graphconfig={"ymin":decay_coherence_min,"ymax":decay_coherence_max}
custom_decay_coherence=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########srtheo_cat##########CAT
from .ngstrat.naive import StratNaiveCategoryPlosOne
strat_srtheo_cat = StratNaiveCategoryPlosOne()
def srtheo_cat(pop,**kwargs):
	fail = 0
	succ = 0
	for i in range(100):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		agent1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		v1 = agent1._vocabulary
		v2 = agent2._vocabulary
		ct = next(agent1._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2))
		#ms = random.choice(ct)
		ms = strat_srtheo_cat.pick_m(v1,agent1._memory,ct)
		w = strat_srtheo_cat.pick_w(ms,v1,agent1._memory,ct)
		mh = strat_srtheo_cat.guess_m(w,v2,agent2._memory,ct)


		#ct_maxinf = max([-1] + [m for m in ct if m < ms])
		#ct_minsup = min([2] + [m for m in ct if m > ms])
		#iv = v1.get_category(ms)
		#if iv.begin < ct_maxinf or iv.end >= ct_minsup:
		#	w = v1.get_new_unknown_w()
		#else:
		#	w = v1.get_random_known_w(m=ms)
#
#		#ml = []
#		#for m in ct:
#		#	if w in v2.get_known_words(m):
#		#		ml.append(m)
#		#if not ml:
#		#	mh = None
#		#else:
#		#	mh = random.choice(ml)
		##print ct, ms, iv, ct_maxinf, ct_minsup, w, v2.get_known_words(ms), ml, mh
		if agent2.eval_success(ms=ms, w=w, mh=mh,context=ct):
			succ += 1
		else:
			fail += 1
		v1.del_cache()
		v2.del_cache()
	return succ/float(succ+fail)

def srtheo_cat_max(pop):
	return 1

def srtheo_cat_min(pop):
	return 0

FUNC=srtheo_cat
graphconfig={"ymin":srtheo_cat_min,"ymax":srtheo_cat_max}
custom_srtheo_cat=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

###############""srtheo as used in epirob08 paper#############
def srtheo2(pop,**kwargs):
	C = np.zeros((pop.get_W(),pop.get_M()))
	best_scores = np.zeros((pop.get_M(),pop._size))
	for ag in range(len(pop._agentlist)):
		for m in range(pop.get_M()):
			try:
				best_scores[m,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_row(m))
			except TypeError:
				print('e')
				print(pop._agentlist[ag]._vocabulary.get_row(m))
				print(max(pop._agentlist[ag]._vocabulary.get_row(m)))
				print('e')
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_row(m))
	n_meanings_used = 0
	for a in range(pop._size):
		for meaning in range(pop.get_M()):
			score = best_scores[meaning,a]
			if score > 0:
				n_meanings_used += 1
				words = pop._agentlist[a]._vocabulary.get_known_words(m=meaning,option='max')
				if words:
					word = words[0]
					C[word,meaning] += 1
	C = C/float(pop._size)
	n_meanings_used = n_meanings_used/float(pop._size)

	n_words_used = 0
	D = np.zeros((pop.get_W(),pop.get_M()))
	best_scores = np.zeros((pop.get_W(),pop._size))
	for ag in range(len(pop._agentlist)):
		for w in range(pop.get_W()):
			try:
				best_scores[w,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_column(w))
			except TypeError:
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_column(w))
	for a in range(pop._size):
		for word in range(pop.get_W()):
			score = best_scores[word,a]
			if score > 0:
				n_words_used += 1
				meanings = pop._agentlist[a]._vocabulary.get_known_meanings(w=word,option='max')
				if meanings:
					meaning = meanings[0]
					D[word,meaning] += 1.
	D = D/float(pop._size)
	n_words_used = n_words_used/float(pop._size)

	return sum(sum(np.multiply(C,D)))/float(pop.get_M())


def srtheo2_max(pop):
	return 1

def srtheo2_min(pop):
	return 0

FUNC=srtheo2
graphconfig={"ymin":srtheo2_min,"ymax":srtheo2_max}
custom_srtheo2=custom_func.CustomFunc(FUNC,"population",**graphconfig)

###############""srtheo as used in epirob08 paper#############
def srtheo3(pop,**kwargs):
	C = np.zeros((pop.get_W(),pop.get_M()))
	best_scores = np.zeros((pop.get_M(),pop._size))
	for ag in range(len(pop._agentlist)):
		for m in range(pop.get_M()):
			try:
				best_scores[m,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_row(m))
			except TypeError:
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_row(m))
	n_meanings_used = 0
	for a in range(pop._size):
		for meaning in range(pop.get_M()):
			score = best_scores[meaning,a]
			if score > 0:
				n_meanings_used += 1
				words = pop._agentlist[a]._vocabulary.get_known_words(m=meaning,option='max')
				#word = word[0]
				#C[word,meaning] += 1
				if words:
					for word in words:
						C[word,meaning] += 1./len(words)
	C = C/float(pop._size)
	n_meanings_used = n_meanings_used/float(pop._size)

	D = np.zeros((pop.get_W(),pop.get_M()))
	best_scores = np.zeros((pop.get_W(),pop._size))
	for ag in range(len(pop._agentlist)):
		for w in range(pop.get_W()):
			try:
				best_scores[w,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_column(w))
			except TypeError:
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_column(w))
	n_words_used = 0
	for a in range(pop._size):
		for word in range(pop.get_W()):
			score = best_scores[word,a]
			if score > 0:
				n_words_used += 1
				meanings = pop._agentlist[a]._vocabulary.get_known_meanings(w=word,option='max')
				#meaning = meaning[0]
				#D[word,meaning] += 1
				if meanings:
					for meaning in meanings:
						D[word,meaning] += 1./len(meanings)
	D = D/float(pop._size)
	n_words_used = n_words_used/float(pop._size)

	return sum(sum(np.multiply(C,D)))/float(pop.get_M())


def srtheo3_max(pop):
	return 1

def srtheo3_min(pop):
	return 0

FUNC=srtheo3
graphconfig={"ymin":srtheo3_min,"ymax":srtheo3_max}
custom_srtheo3=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropydistrib##########

def entropydistrib(pop,**kwargs):
	if not hasattr(pop._agentlist[0]._vocabulary,'_content'):
		raise ValueError('this measure is not implemented for this type of vocabulary')
	tempmat=np.matrix(np.zeros((pop.get_M(),pop.get_W())))
	for ag in pop._agentlist:
		tempmat=tempmat+ag._vocabulary.get_content()
	ans=0
	for m in range(pop.get_M()):
		temp=pop._size
		for w in range(pop.get_W()):
			temp=temp-tempmat[m,w]
		for w in range(pop.get_W()):
			tempmat[m,w]=(tempmat[m,w]+temp/pop.get_W())/pop._size
			if tempmat[m,w]!=0:
				ans-=tempmat[m,w]*np.log2(tempmat[m,w])
	return ans

def entropydistrib_max(pop):
	return pop.get_M()*np.log2(pop.get_W())

def entropydistrib_min(pop):
	return 0

FUNC=entropydistrib
graphconfig={"ymin":entropydistrib_min,"ymax":entropydistrib_max}
custom_entropydistrib=custom_func.CustomFunc(FUNC,"population",tags=["old_voc"],**graphconfig)

#########line_border##########

def line_border(pop,**kwargs):
	m = pop._agentlist[0]._vocabulary.get_accessible_meanings()[0]
	w1_l = pop._agentlist[0]._vocabulary.get_known_words(m=m)
	w2_l = pop._agentlist[-1]._vocabulary.get_known_words(m=m)
	if len(w1_l) == 1 and len(w2_l) == 1 and w1_l[0] == w2_l[0]:
		return np.nan
	else:
		if len(w1_l) != 1:
			x1 = 0.
		else:
			for i1 in range(len(pop._agentlist)):
				if pop._agentlist[i1]._vocabulary.get_known_words(m=m) == w1_l:
					x1 = i1
				elif w1_l[0] not in pop._agentlist[i1]._vocabulary.get_known_words(m=m):
					break
		if len(w2_l) != 1:
			x2 = pop._size
		else:
			for i2 in range(len(pop._agentlist)):
				if pop._agentlist[-1-i2]._vocabulary.get_known_words(m=m) == w2_l:
					x2 = pop._size - i2
				elif w2_l[0] not in pop._agentlist[-1-i2]._vocabulary.get_known_words(m=m):
					break
		return (x2+x1 - pop._size)*0.5

def line_border_max(pop):
	return pop._size/2.

def line_border_min(pop):
	return -pop._size/2.

FUNC=line_border
graphconfig={"ymin":line_border_min,"ymax":line_border_max}
custom_line_border=custom_func.CustomFunc(FUNC,"population",tags=["halfline"],**graphconfig)

#########line_border_width##########

def line_border_width(pop,**kwargs):
	m = pop._agentlist[0]._vocabulary.get_accessible_meanings()[0]
	w1_l = pop._agentlist[0]._vocabulary.get_known_words(m=m)
	w2_l = pop._agentlist[-1]._vocabulary.get_known_words(m=m)
	if len(w1_l) == 1 and len(w2_l) == 1 and w1_l[0] == w2_l[0]:
		return np.nan
	else:
		if len(w1_l) != 1:
			x1 = 0.
		else:
			for i1 in range(len(pop._agentlist)):
				if pop._agentlist[i1]._vocabulary.get_known_words(m=m) == w1_l:
					x1 = i1
				elif w1_l[0] not in pop._agentlist[i1]._vocabulary.get_known_words(m=m):
					break
		if len(w2_l) != 1:
			x2 = pop._size
		else:
			for i2 in range(len(pop._agentlist)):
				if pop._agentlist[-1-i2]._vocabulary.get_known_words(m=m) == w2_l:
					x2 = pop._size - i2
				elif w2_l[0] not in pop._agentlist[-1-i2]._vocabulary.get_known_words(m=m):
					break
		return (x2-x1)-1

def line_border_width_max(pop):
	return pop._size/2.

def line_border_width_min(pop):
	return 0

FUNC=line_border_width
graphconfig={"ymin":line_border_width_min,"ymax":line_border_width_max}
custom_line_border_width=custom_func.CustomFunc(FUNC,"population",tags=["halfline"],**graphconfig)

#########line_border_abs##########

def line_border_abs(pop,**kwargs):
	return np.abs(line_border(pop,**kwargs))

def line_border_abs_max(pop):
	return pop._size/2.

def line_border_abs_min(pop):
	return 0

FUNC=line_border_abs
graphconfig={"ymin":line_border_abs_min}#,"ymax":line_border_abs_max}
custom_line_border_abs=custom_func.CustomFunc(FUNC,"population",tags=["halfline"],**graphconfig)

#########line_border_squared##########

def line_border_squared(pop,**kwargs):
	return (line_border(pop,**kwargs))**2

def line_border_squared_max(pop):
	return pop._size/2.

def line_border_squared_min(pop):
	return 0

FUNC=line_border_squared
graphconfig={"ymin":line_border_squared_min}#,"ymax":line_border_squared_max}
custom_line_border_squared=custom_func.CustomFunc(FUNC,"population",tags=["halfline"],**graphconfig)

#########overlap##########CAT

def overlap(pop,**kwargs):
	n_r = min((pop._size**2),100)
	overlap_val = 0
	for i in range(n_r):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		ag1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		ag2 = pop._agentlist[pop.get_index_from_id(agent2_id)]


		ivt1 = []
		for iv in sorted(ag1._vocabulary._content_coding):
			ivt1.append(iv.begin)
		ivt1.append(1.)
		ivt2 = []
		for iv in sorted(ag2._vocabulary._content_coding):
			ivt2.append(iv.begin)
		ivt2.append(1.)
		ivt1.sort()
		ivt2.sort()
		ivto = sorted(ivt1 + ivt2)
		ovsum1 =  sum([(ivt1[k+1]-ivt1[k])**2 for k in range(len(ivt1)-1)])
		ovsum2 =  sum([(ivt2[k+1]-ivt2[k])**2 for k in range(len(ivt2)-1)])
		if ivto == IntervalTree([Interval(0,1)]):
			ovsumo = 0
		else:
			ovsumo =  sum([(ivto[k+1]-ivto[k])**2 for k in range(len(ivto)-1)])

#		ivt1 = copy.deepcopy(ag1._vocabulary._content_coding)
#		ivt2 = copy.deepcopy(ag2._vocabulary._content_coding)
#		ivto = copy.deepcopy(ag1._vocabulary._content_coding)
#		ivto.union(ivt2)
#		ivto.split_overlaps()
#		ivto.merge_overlaps()
#		ovsum1 =  sum([(iv.end - iv.begin)**2 for iv in ivt1])
#		ovsum2 =  sum([(iv.end - iv.begin)**2 for iv in ivt2])
#		ovsumo =  sum([(iv.end - iv.begin)**2 for iv in ivto])
		overlap_val += (2*ovsumo/float(ovsum1 + ovsum2))
	return overlap_val / float(n_r)

def overlap_max(pop):
	return 1

def overlap_min(pop):
	return 0

FUNC=overlap
graphconfig={"ymin":overlap_min,"ymax":overlap_max}
custom_overlap=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

#########overlap_semantic##########CAT

def overlap_semantic(pop,**kwargs):
	n_r = min((pop._size**2)/2,100)
	overlap_val = 0
	for i in range(n_r):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		ag1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		ag2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		ivt1 = []
		data = None
		for iv in sorted(ag1._vocabulary._content_coding):
			val = max([0]+list(iv.data.values()))
			data1 = [w for w,v in list(iv.data.items()) if v == val]
			if data != data1:
				ivt1.append(iv.begin)
				data = copy.copy(data1)
		ivt1.append(1.)
		ivt2 = []
		data = None
		for iv in sorted(ag2._vocabulary._content_coding):
			val = max([0]+list(iv.data.values()))
			data1 = [w for w,v in list(iv.data.items()) if v == val]
			if data != data1:
				ivt2.append(iv.begin)
				data = copy.copy(data1)
		ivt2.append(1.)
		ivto = sorted(ivt1 + ivt2)
		ovsum1 =  sum([(ivt1[k+1]-ivt1[k])**2 for k in range(len(ivt1)-1)])
		ovsum2 =  sum([(ivt2[k+1]-ivt2[k])**2 for k in range(len(ivt2)-1)])
		if ivto == IntervalTree([Interval(0,1)]):
			ovsumo = 0
		else:
			ovsumo =  sum([(ivto[k+1]-ivto[k])**2 for k in range(len(ivto)-1)])
		overlap_val += (2*ovsumo/float(ovsum1 + ovsum2))
	return overlap_val / float(n_r)

def overlap_semantic_max(pop):
	return 1

def overlap_semantic_min(pop):
	return 0

FUNC=overlap_semantic
graphconfig={"ymin":overlap_semantic_min,"ymax":overlap_semantic_max}
custom_overlap_semantic=custom_func.CustomFunc(FUNC,"population",tags='category',**graphconfig)

#########nb_inventions##########

def nb_inventions(pop,**kwargs):
	return sum([agent._memory['inventions']['nb_inventions'] for agent in pop._agentlist if 'inventions' in list(agent._memory.keys())])

def nb_inventions_max(pop):
	return pop.get_M()

def nb_inventions_min(pop):
	return 0


FUNC=nb_inventions
graphconfig={"ymin":nb_inventions_min}#,"ymax":nb_inventions_max}
custom_nb_inventions =custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########nb_inventions_per_known_m##########

def nb_inventions_per_known_m(pop,**kwargs):
	val = nb_inventions(pop)
	nm = N_meanings_pop(pop)
	if nm == 0:
		return 0
	else:
		return val*1./N_meanings_pop(pop)

def nb_inventions_per_known_m_max(pop):
	return pop.get_M()

def nb_inventions_per_known_m_min(pop):
	return 0


FUNC=nb_inventions_per_known_m
graphconfig={"ymin":nb_inventions_per_known_m_min}#,"ymax":nb_inventions_per_known_m_max}
custom_nb_inventions_per_known_m =custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_meanings_pop##########

def N_meanings_pop(pop,**kwargs):
	ans = 0
	for m in pop.env.m_list:
		for ag in pop._agentlist:
			if m in ag._vocabulary.get_known_meanings():
				ans += 1
				break
	return ans

def N_meanings_pop_max(pop):
	return pop.get_M()

def N_meanings_pop_min(pop):
	return 0


FUNC=N_meanings_pop
graphconfig={"ymin":N_meanings_pop_min,"ymax":N_meanings_pop_max}
custom_N_meanings_pop =custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_meanings_pop_0inv##########

def N_meanings_pop_0inv(pop,**kwargs):
	return pop.get_M()-N_meanings_pop(pop)

def N_meanings_pop_0inv_max(pop):
	return pop.get_M()

def N_meanings_pop_0inv_min(pop):
	return 0


FUNC=N_meanings_pop_0inv
graphconfig={"ymin":N_meanings_pop_0inv_min,"ymax":N_meanings_pop_0inv_max}
custom_N_meanings_pop_0inv =custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_meanings_pop_1inv##########

def N_meanings_pop_1inv(pop,**kwargs):
	return len([True for m in pop.env.m_list if nb_inventions_per_m(m,pop=pop) == 1])

def N_meanings_pop_1inv_max(pop):
	return pop.get_M()

def N_meanings_pop_1inv_min(pop):
	return 0


FUNC=N_meanings_pop_1inv
graphconfig={"ymin":N_meanings_pop_1inv_min,"ymax":N_meanings_pop_1inv_max}
custom_N_meanings_pop_1inv =custom_func.CustomFunc(FUNC,"population",**graphconfig)
#########N_meanings_pop_2inv##########

def N_meanings_pop_2inv(pop,**kwargs):
	return len([True for m in pop.env.m_list if nb_inventions_per_m(m,pop=pop) == 2])

def N_meanings_pop_2inv_max(pop):
	return pop.get_M()

def N_meanings_pop_2inv_min(pop):
	return 0


FUNC=N_meanings_pop_2inv
graphconfig={"ymin":N_meanings_pop_2inv_min,"ymax":N_meanings_pop_2inv_max}
custom_N_meanings_pop_2inv =custom_func.CustomFunc(FUNC,"population",**graphconfig)
#########N_meanings_pop_3ormoreinv##########

def N_meanings_pop_3ormoreinv(pop,**kwargs):
	return len([True for m in pop.env.m_list if nb_inventions_per_m(m,pop=pop) >= 3])

def N_meanings_pop_3ormoreinv_max(pop):
	return pop.get_M()

def N_meanings_pop_3ormoreinv_min(pop):
	return 0


FUNC=N_meanings_pop_3ormoreinv
graphconfig={"ymin":N_meanings_pop_3ormoreinv_min,"ymax":N_meanings_pop_3ormoreinv_max}
custom_N_meanings_pop_3ormoreinv =custom_func.CustomFunc(FUNC,"population",**graphconfig)
#########N_words_pop##########

def N_words_pop(pop,**kwargs):
	ans = 0
	for w in pop.env.w_list:
		for ag in pop._agentlist:
			if w in ag._vocabulary.get_known_words():
				ans += 1
				break
	return ans

def N_words_pop_max(pop):
	return pop.get_W()

def N_words_pop_min(pop):
	return 0


FUNC=N_words_pop
graphconfig={"ymin":N_words_pop_min,"ymax":N_words_pop_max}
custom_N_words_pop =custom_func.CustomFunc(FUNC,"population",**graphconfig)
#########weight_over_degree##########

# def weight_over_degree(pop,**kwargs):
# 	G = nx_utils.build_nx_graph(pop._agentlist)
# 	values = []
# 	for ag in pop._agentlist:
# 		weight = 0
# 		for ed in G.edges(ag._id):
# 			weight += ed['weight']
# 		if weight != 0 :
# 			values.append(weight/G.degree(ag._id))
# 		else:
# 			values.append(0)
# 	return mean(values)

# def weight_over_degree_max(pop):
# 	return 1

# def weight_over_degree_min(pop):
# 	return 0


# FUNC=weight_over_degree
# graphconfig={"ymin":weight_over_degree_min,"ymax":weight_over_degree_max}
# custom_weight_over_degree =custom_func.CustomFunc(FUNC,"population",**graphconfig)

############################	LEVEL TIME ############################

#### 	INPUT:		expe, **progress_info
####	OUTPUT:		vector (size same as _T)

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"experiment",**graphconfig)

#########interactions_per_agent##########

def interactions_per_agent(exp,**kwargs):
	return list(np.array(exp._T)*2./exp._poplist[0]._size)

def interactions_per_agent_max(exp):
	return max(exp._T)*2./exp._poplist[0]._size

def interactions_per_agent_min(exp):
	return min(exp._T)*2./exp._poplist[0]._size


FUNC=interactions_per_agent
graphconfig={"ymin":interactions_per_agent_min,"ymax":interactions_per_agent_max}
custom_interactions_per_agent =custom_func.CustomFunc(FUNC,"time",**graphconfig)


############################	LEVEL EXP ############################

#### 	INPUT:		expe, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"exp",**graphconfig)



#########product_maxmem_convtime##########

def product_maxmem_convtime(exp,X=0,**kwargs):

	max_mem_val = exp.graph('max_mem_conv',autocommit=False)._Y[0][0]
	conv_time_val = exp.graph('conv_time',autocommit=False)._Y[0][0]
	return [max_mem_val*conv_time_val]

def product_maxmem_convtime_min(exp):
	return 0

FUNC = product_maxmem_convtime

graphconfig = {"ymin":product_maxmem_convtime_min}#,"ymax":product_maxmem_convtime_max}
custom_product_maxmem_convtime =custom_func.CustomFunc(FUNC,"exp",**graphconfig)


#########srtheo_end##########

def srtheo_end(exp,X=0,**kwargs):

	sr_gr = exp.graph('srtheo',autocommit=False)
	return [sr_gr._Y[0][-1]]

def srtheo_end_min(exp):
	return 0

def srtheo_end_max(exp):
	return 1.

FUNC = srtheo_end

graphconfig = {"ymin":srtheo_end_min,"ymax":srtheo_end_max}
custom_srtheo_end =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########srtheo_end_smooth##########

def srtheo_end_smooth(exp,X=0,**kwargs):

	sr_gr = exp.graph('srtheo',autocommit=False)
	if len(sr_gr._Y[0]) < 5:
		return [np.mean(sr_gr._Y[0])]
	else:
		return [np.mean(sr_gr._Y[0][-5:])]

def srtheo_end_smooth_min(exp):
	return 0

def srtheo_end_smooth_max(exp):
	return 1.

FUNC = srtheo_end_smooth

graphconfig = {"ymin":srtheo_end_smooth_min,"ymax":srtheo_end_smooth_max}
custom_srtheo_end_smooth =custom_func.CustomFunc(FUNC,"exp",**graphconfig)
#########decay_end_smooth##########

def decay_end_smooth(exp,X=0,**kwargs):

	sr_gr = exp.graph('decay_coherence',autocommit=False)
	if len(sr_gr._Y[0]) < 5:
		return [np.mean(sr_gr._Y[0])]
	else:
		return [np.mean(sr_gr._Y[0][-5:])]

def decay_end_smooth_min(exp):
	return 0

def decay_end_smooth_max(exp):
	return 1.

FUNC = decay_end_smooth

graphconfig = {"ymin":decay_end_smooth_min,"ymax":decay_end_smooth_max}
custom_decay_end_smooth =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_mem##########

def max_mem(exp,X=0,**kwargs):

	mem = exp.graph('Nlink',autocommit=False)
	return [max(mem._Y[0])]

def max_mem_min(exp):
	return 0

FUNC = max_mem

graphconfig = {"ymin":max_mem_min}#,"ymax":max_mem_max}
custom_max_mem =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_mem_conv##########

def max_mem_conv(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	sr = sr_gr._Y[0][-1]
	if sr >= thresh:
		return max_mem(exp,X=X,**kwargs)
	else:
		return [np.nan]


FUNC = max_mem_conv

graphconfig = {"ymin":max_mem_min}#,"ymax":max_mem_max}
custom_max_mem_conv = custom_func.CustomFunc(FUNC,"exp",**graphconfig)



#########max_N_d##########

def max_N_d(exp,X=0,**kwargs):

	mem = exp.graph('N_d',autocommit=False)
	return [max(mem._Y[0])]

def max_N_d_min(exp):
	return 0

FUNC = max_N_d

graphconfig = {"ymin":max_N_d_min}#,"ymax":max_N_d_max}
custom_max_N_d =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_N_d_conv##########

def max_N_d_conv(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	sr = sr_gr._Y[0][-1]
	if sr >= thresh:
		return max_N_d(exp,X=X,**kwargs)
	else:
		return [np.nan]


FUNC = max_N_d_conv

graphconfig = {"ymin":max_N_d_min}#,"ymax":max_N_d_max}
custom_max_N_d_conv = custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########conv_time##########

def conv_time(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	sr = sr_gr._Y[0]
	for i in range(len(sr)):
		if sr[i] >= thresh:
			return [sr_gr._X[0][i]]
	return [np.nan]


def conv_time_max(exp):
	return exp._T[-1]

def conv_time_min(exp):
	return 0

FUNC = conv_time

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########conv_time2##########

def conv_time2(exp,X=0,thresh=1.,**kwargs):
	Nd_gr = exp.graph('N_d',autocommit=False)
	Nd = Nd_gr._Y[0]
	Nm_gr = exp.graph('N_meanings',autocommit=False)
	Nm = Nm_gr._Y[0]
	Nw_gr = exp.graph('N_words',autocommit=False)
	Nw = Nw_gr._Y[0]
	M = N_meanings_max(exp._poplist.get_last())
	for i in range(len(Nd)):
		if Nm[i] == M and Nd[i] == M and Nw[i] == M:
			return [Nd_gr._X[0][i]]
	return [np.nan]

def conv_time2_max(exp):
	return exp._T[-1]

def conv_time2_min(exp):
	return 0

FUNC = conv_time2

graphconfig = {"ymin":conv_time2_min,"ymax":conv_time2_max}
custom_conv_time2 =custom_func.CustomFunc(FUNC,"exp",**graphconfig)
#########decay_time##########

def decay_time(exp,X=0,**kwargs):
	vect = exp.graph('decay_coherence',autocommit=False)
	val = exp.graph('decay_coherence',autocommit=False)._Y[0][-1]
	for i in range(len(vect._Y[0])):
		if vect._Y[0][i] <= val:
			return [vect._X[0][i]]
	return [np.nan]


def decay_time_max(exp):
	return exp._T[-1]

def decay_time_min(exp):
	return 0

FUNC = decay_time

graphconfig = {"ymin":decay_time_min,"ymax":decay_time_max}
custom_decay_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########decay_time_smooth##########

def decay_time_smooth(exp,X=0,**kwargs):
	val = exp.graph('decay_end_smooth',autocommit=False)._Y[0][0]
	vect = exp.graph('decay_coherence',autocommit=False)
	for i in range(len(vect._Y[0])):
		if vect._Y[0][i] <= val:
			return [vect._X[0][i]]
	return [np.nan]

FUNC = decay_time_smooth

graphconfig = {"ymin":decay_time_min,"ymax":decay_time_max}
custom_decay_time_smooth =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########block_time##########

def block_time(exp,X=0,**kwargs):
	Nd_gr = exp.graph('N_d',autocommit=False)
	Nd = Nd_gr._Y[0]
	Nm_gr = exp.graph('N_meanings',autocommit=False)
	Nm = Nm_gr._Y[0]
	M = N_meanings_max(exp._poplist.get_last())
	for i in range(len(Nd)):
		if Nm[i] == M and Nd[i] == M:
			return [Nd_gr._X[0][i]]
	return [np.nan]

def block_time_max(exp):
	return exp._T[-1]

def block_time_min(exp):
	return 0

FUNC = block_time

graphconfig = {"ymin":block_time_min,"ymax":block_time_max}
custom_block_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########homonymy_block##########

def homonymy_block(exp,X=0,**kwargs):
	Nd_gr = exp.graph('N_d',autocommit=False)
	Nd = Nd_gr._Y[0]
	Nm_gr = exp.graph('N_meanings',autocommit=False)
	Nm = Nm_gr._Y[0]
	hom_gr = exp.graph('homonymy',autocommit=False)
	hom = hom_gr._Y[0]
	M = N_meanings_max(exp._poplist.get_last())
	if Nm[-1] == M and Nd[-1] == M:
		return [hom_gr._Y[0][-1]]
	else:
		return [np.nan]

def homonymy_block_max(exp):
	return exp._T[-1]

def homonymy_block_min(exp):
	return 0

FUNC = homonymy_block

graphconfig = {"ymin":homonymy_block_min}#,"ymax":homonymy_block_max}
custom_homonymy_block =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_N_d_time##########

def max_N_d_time(exp,X=0,thresh=1.,**kwargs):
	N_d_gr = exp.graph('N_d',autocommit=False)
	N_d_vec = N_d_gr._Y[0]
	val = max(N_d_vec)
	for i in range(len(N_d_vec)-1):
		if N_d_vec[i] == val:
			return [N_d_gr._X[0][i]]
	return [np.nan]


def max_N_d_time_max(exp):
	return exp._T[-1]

def max_N_d_time_min(exp):
	return 0

FUNC = max_N_d_time

graphconfig = {"ymin":max_N_d_time_min,"ymax":max_N_d_time_max}
custom_max_N_d_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_Nlink_time##########

def max_Nlink_time(exp,X=0,thresh=1.,**kwargs):
	Nlink_gr = exp.graph('Nlink',autocommit=False)
	Nlink_vec = Nlink_gr._Y[0]
	val = max(Nlink_vec)
	for i in range(len(Nlink_vec)-1):
		if Nlink_vec[i] == val:
			return [Nlink_gr._X[0][i]]
	return [np.nan]


def max_Nlink_time_max(exp):
	return exp._T[-1]

def max_Nlink_time_min(exp):
	return 0

FUNC = max_Nlink_time

graphconfig = {"ymin":max_Nlink_time_min,"ymax":max_Nlink_time_max}
custom_max_Nlink_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########tdiff_d##########

def tdiff_d(exp,X=0,thresh=1.,**kwargs):
	val1 = exp.graph('max_N_d_time',autocommit=False)._Y[0][0]
	val2 = exp.graph('conv_time2',autocommit=False)._Y[0][0]
	return [val2-val1]


def tdiff_d_max(exp):
	return exp._T[-1]

def tdiff_d_min(exp):
	return 0

FUNC = tdiff_d

graphconfig = {"ymin":tdiff_d_min,"ymax":tdiff_d_max}
custom_tdiff_d =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########tdiff_w##########

def tdiff_w(exp,X=0,thresh=1.,**kwargs):
	val1 = exp.graph('max_Nlink_time',autocommit=False)._Y[0][0]
	val2 = exp.graph('conv_time2',autocommit=False)._Y[0][0]
	return [val2-val1]


def tdiff_w_max(exp):
	return exp._T[-1]

def tdiff_w_min(exp):
	return 0

FUNC = tdiff_w

graphconfig = {"ymin":tdiff_w_min,"ymax":tdiff_w_max}
custom_tdiff_w =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########tdiff_wd##########

def tdiff_wd(exp,X=0,thresh=1.,**kwargs):
	val1 = exp.graph('max_N_d_time',autocommit=False)._Y[0][0]
	val2 = exp.graph('max_Nlink_time',autocommit=False)._Y[0][0]
	return [val2-val1]


def tdiff_wd_max(exp):
	return exp._T[-1]

def tdiff_wd_min(exp):
	return 0

FUNC = tdiff_wd

graphconfig = {"ymin":tdiff_wd_min,"ymax":tdiff_wd_max}
custom_tdiff_wd =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########conv_time_plus_srtheo##########

def conv_time_plus_srtheo(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	sr = sr_gr._Y[0]
	for i in range(len(sr)):
		if sr[i] >= thresh:
			break
	return [sr_gr._X[0][i]+(1.-sr_gr._Y[0][i])]


FUNC = conv_time_plus_srtheo

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time_plus_srtheo =custom_func.CustomFunc(FUNC,"exp",**graphconfig)
#########srtheo_and_block_time##########

def srtheo_and_block_time(exp,X=0,thresh=1.,**kwargs):
	sr_val = -1
	sr_gr = exp.graph('srtheo',autocommit=False)
	bt_gr = exp.graph('block_time',autocommit=False)
	bt_val = bt_gr._Y[0][0]
	for i in range(len(sr_gr._X[0])):
		if sr_gr._X[0][i] == bt_val:
			sr_val = sr_gr._Y[0][i]
			break
	if sr_val == -1:
		sr_val = sr_gr._Y[0][-1]
	return [(-sr_val,bt_val)]


FUNC = srtheo_and_block_time

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_srtheo_and_block_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)
#########conv_time2_Nm_srtheo##########

def conv_time2_Nm_srtheo(exp,X=0,thresh=1.,**kwargs):
	sr_val = -1
	sr_gr = exp.graph('srtheo',autocommit=False)
	ct2_gr = exp.graph('conv_time2',autocommit=False)
	Nm_gr = exp.graph('N_meanings',autocommit=False)
	ct_val = ct2_gr._Y[0][-1]
	for i in range(len(sr_gr._X[0])):
		if sr_gr._X[0][i] == ct_val:
			sr_val = sr_gr._Y[0][i]
			Nm = Nm_gr._Y[0][i]
			break
	if sr_val == -1:
		sr_val =  sr_gr._Y[0][-1]
		Nm = Nm_gr._Y[0][-1]
	return [(ct_val,-Nm,-sr_val)]


FUNC = conv_time2_Nm_srtheo

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time2_Nm_srtheo =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########partial_conv_time##########

def partial_conv_time(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	sr = sr_gr._Y[0]
	for i in range(len(sr)):
		if sr[i] >= 0.9*thresh:
			return [sr_gr._X[0][i]]
	return [np.nan]


FUNC = partial_conv_time

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_partial_conv_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_mem_conv_threshold##########

def max_mem_conv_threshold(exp,X=0,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	thresh = sr_gr._Y[0][-1]
	return max_mem(exp,X=X,thresh=thresh,**kwargs)


FUNC = max_mem_conv_threshold

graphconfig = {"ymin":max_mem_min}#,"ymax":max_mem_max}
custom_max_mem_conv_threshold = custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########conv_time_threshold##########

def conv_time_threshold(exp,X=0,**kwargs):
	thresh = exp.graph('srtheo_end',autocommit=False)._Y[0][0]
	return conv_time(exp,X=X,thresh=thresh,**kwargs)

FUNC = conv_time_threshold

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time_threshold =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########conv_time_end_value##########

def conv_time_threshold_smooth(exp,X=0,**kwargs):
	thresh = exp.graph('srtheo_end_smooth',autocommit=False)._Y[0][0]
	return conv_time(exp,X=X,thresh=thresh,**kwargs)

FUNC = conv_time_threshold_smooth

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time_threshold_smooth =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########partial_conv_time_threshold##########

def partial_conv_time_threshold(exp,X=0,**kwargs):
	sr_gr = exp.graph('srtheo',autocommit=False)
	thresh = sr_gr._Y[0][-1]
	return partial_conv_time(exp,X=X,thresh=thresh,**kwargs)


FUNC = partial_conv_time_threshold

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_partial_conv_time_threshold = custom_func.CustomFunc(FUNC,"exp",**graphconfig)

################################################################

#########exec_time_total##########

def exec_time_total(exp,X=0,**kwargs):
	return [exp._exec_time[-1]]


FUNC = exec_time_total

def exec_time_total_min(exp):
	return 0

graphconfig = {"ymin":exec_time_total_min}
custom_exec_time_total = custom_func.CustomFunc(FUNC,"exp",**graphconfig)

################################################################







