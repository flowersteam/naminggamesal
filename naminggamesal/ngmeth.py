#!/usr/bin/python
import copy
import numpy as np
import math
import random
import networkx as nx
from intervaltree import IntervalTree,Interval
import scipy

#from numpy.linalg import norm

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph
from .ngpop import Population

def pop_ize(func):
	def out_func(pop,**kwargs):
		tempNlist=[]
		agentlist=pop._agentlist
		for i in range(0,len(agentlist)):
			tempNlist.append(func(agentlist[i]))
			mean=np.mean(tempNlist)
			std=np.std(tempNlist)
		return [mean,std,tempNlist]
	out_func.__name__=func.__name__+"_mean"
	return out_func



############################	LEVEL AGENT ############################

#### 	INPUT:		agent , **progress_info
####	OUTPUT:		[mean,std,(tempNlist)]

#	FUNC_BIS=pop_ize(FUNC)
#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Nlink##########

def Nlink(agent,**kwargs):
	tempmat = copy.deepcopy(agent.get_vocabulary_content())
	tempmat[tempmat>0] = 1
	return np.sum(tempmat)

def Nlink_max(pop):
	return pop._M * pop._W

def Nlink_min(pop):
	return 0


FUNC=Nlink
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Nlink_min}#,"ymax":Nlink_max}
custom_Nlink =custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


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
custom_new_entropy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)
#########entropy_time_scale##########

def entropy_time_scale(agent=None,mem=None,voc=None,m=None,w=None,**kwargs):
	if mem is None:
		mem = agent._memory
		if voc is None:
			voc = agent._vocabulary
	entr = 0

	if m is None:
		mat = mem['interaction_count_m']
	else:
		mat = mem['interaction_count_m'][m,:]
	entr +=  scipy.special.entr(mat).sum()

	if w is None:
		mat = mem['interaction_count_w']
	else:
		mat = mem['interaction_count_w'][:,w]
	entr +=  scipy.special.entr(mat).sum()

	return entr




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
custom_new_entropy_success=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

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
custom_new_entropy_withvoc=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


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
custom_new_entropy_globalnorm=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


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
custom_new_entropy_success_rate=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########transinformation##########

def voc_transinf(voc):
	M = voc._M
	W = voc._W
	KM = voc.get_known_meanings()
	Mtransinf = len(KM)*np.log2(W)
	for m in KM:
		Mtransinf -= np.log2(len(voc.get_known_words(m=m)))
	return Mtransinf*1./M

def transinformation(agent,**kwargs):
	voc = agent._vocabulary
	return voc_transinf(voc)

def transinformation_max(pop):
	return np.log2(pop._W)

def transinformation_min(pop):
	return 0

FUNC=transinformation
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":transinformation_min,"ymax":transinformation_max}
custom_transinformation=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########connex_components_per_word##########

def connex_components_per_word(agent,**kwargs):
	if agent._vocabulary._content_decoding:
		return sum([len(x) for x in agent._vocabulary._content_decoding.values()])/float(len(agent._vocabulary._content_decoding.keys()))
	else:
		return 0

def connex_components_per_word_max(pop):
	return 1

def connex_components_per_word_min(pop):
	return 0

FUNC=connex_components_per_word
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":connex_components_per_word_min}#,"ymax":connex_components_per_word_max}
custom_connex_components_per_word=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Ncat_percept##########

def Ncat_percept(agent,**kwargs):
	return len(agent._vocabulary._content_coding)

def Ncat_percept_max(pop):
	return 1

def Ncat_percept_min(pop):
	return 0

FUNC=Ncat_percept
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Ncat_percept_min}#,"ymax":Ncat_percept_max}
custom_Ncat_percept=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Ncat_semantic##########

def Ncat_semantic(agent,**kwargs):
	n = 0
	data = None
	for iv in sorted(agent._vocabulary._content_coding):
		val = max([0]+list(iv.data.values()))
		data1 = [w for w,v in iv.data.items() if v == val]
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
custom_Ncat_semantic=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########N_words##########

def N_words(agent,**kwargs):
	if hasattr(agent._vocabulary,'_content_decoding'):
		return len(agent._vocabulary._content_decoding.keys())
	else:
		return len(agent._vocabulary.get_known_words())

def N_words_max(pop):
	if hasattr(pop._agentlist[0]._vocabulary,'_W'):
		return pop._agentlist[0]._vocabulary._W
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
	if hasattr(pop._agentlist[0]._vocabulary,'_M'):
		return pop._agentlist[0]._vocabulary._M
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
		return Nlink(agent)/len(agent._vocabulary.get_known_meanings())

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


#########cat_synonymy##########

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
custom_cat_synonymy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########norm_std_Ncat##########

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
custom_norm_std_Ncat=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########norm_std_Npercept##########

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
custom_norm_std_Npercept=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########dist_threshold##########

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
custom_dist_threshold=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########entropy##########

def tempentropy(MM,WW):
	a=0
	for i in range(int(WW-MM+1),int(WW+1)):
		a+=np.log2(i)
	return a

def entropy(agent,**kwargs):
	m=len(agent._vocabulary.get_known_meanings())
	return tempentropy(agent._M-m,agent._W-m)

def entropy_max(pop):
	return tempentropy(pop._M,pop._W)

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


############################	LEVEL POPULATION ############################

#### 	INPUT:		pop, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_d##########

def N_d(pop,**kwargs):
	tempmat = np.matrix(np.zeros((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat += agent._vocabulary._content
	tempmat[tempmat>0] = 1
	return np.sum(tempmat)

def N_d_max(pop):
	return pop._M*pop._W

def N_d_min(pop):
	return 0

FUNC=N_d
graphconfig={"ymin":N_d_min}#,"ymax":N_d_max}
custom_N_d=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_d_m##########

def N_d_m(pop,**kwargs):
	tempmat = np.matrix(np.zeros((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat += agent._vocabulary._content
	tempmat[tempmat>0] = 1
	return np.sum(tempmat[0,:])

def N_d_m_max(pop):
	return pop._W

def N_d_m_min(pop):
	return 0

FUNC=N_d_m
graphconfig={"ymin":N_d_m_min}#,"ymax":N_d_m_max}
custom_N_d_m=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_d_m_ag##########

def N_d_m_ag(pop,**kwargs):
	tempmat = np.matrix(np.zeros((pop._M,pop._W)))
	agent = pop._agentlist[0]
	tempmat += agent._vocabulary._content
	tempmat[tempmat>0] = 1
	return np.sum(tempmat[0,:])

def N_d_m_ag_max(pop):
	return pop._W

def N_d_m_ag_min(pop):
	return 0

FUNC=N_d_m_ag
graphconfig={"ymin":N_d_m_ag_min}#,"ymax":N_d_m_ag_max}
custom_N_d_m_ag=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs##########

def Nlinksurs(pop,**kwargs):
	tempmat=np.matrix(np.ones((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat=np.multiply(tempmat,agent._vocabulary.get_content())
		tempmat[tempmat>0] = 1
	return np.sum(tempmat)

def Nlinksurs_max(pop):
	return pop._M

def Nlinksurs_min(pop):
	return 0

FUNC=Nlinksurs
graphconfig={"ymin":Nlinksurs_min,"ymax":Nlinksurs_max}
custom_Nlinksurs=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs_couples##########

def Nlinksurs_couples(pop,**kwargs):
	tempvalues = []
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		tempm = np.linalg.matrix_rank(np.multiply(agent1.get_vocabulary_content(),agent2.get_vocabulary_content()))
		tempvalues.append(tempm)
	return np.mean(tempvalues)

def Nlinksurs_couples_max(pop):
	return pop._M

def Nlinksurs_couples_min(pop):
	return 0

FUNC=Nlinksurs_couples
graphconfig={"ymin":Nlinksurs_couples_min,"ymax":Nlinksurs_couples_max}
custom_Nlinksurs_couples=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropypop##########

def entropypop(pop,**kwargs):
	m=Nlinksurs(pop)
	return tempentropy(pop._M-m,pop._W-m)

def entropypop_max(pop):
	return tempentropy(pop._M,pop._W)

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
			for m in range(pop._M):
				for w in range(pop._W):
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
		tempvalues.append(tempentropy(pop._M-tempm,pop._W-tempm))
	return np.mean(tempvalues)

def entropycouples_old_max(pop):
	return tempentropy(pop._M,pop._W)

def entropycouples_old_min(pop):
	return 0

FUNC=entropycouples_old
graphconfig={"ymin":entropycouples_old_min,"ymax":entropycouples_old_max}
custom_entropycouples_old=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropycouplesoldnorm##########


def entropycouples_old_norm(pop,**kwargs):
	return 1-(entropycouples(pop)/entropycouples_max(pop))

def entropycouples_old_norm_max(pop):
	return 1

def entropycouples_old_norm_min(pop):
	return 0

FUNC=entropycouples_old_norm
graphconfig={"ymin":entropycouples_old_norm_min,"ymax":entropycouples_old_norm_max}
custom_entropycouples_old_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)

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

#########N_words_pop##########


def N_words_pop(pop,**kwargs):
	words = set()
	for ag in pop._agentlist:
		for w in ag._vocabulary._content_decoding.keys():
			words.add(w)
	return len(words)

def N_words_pop_max(pop):
	return 1

def N_words_pop_min(pop):
	return 0

FUNC=N_words_pop
graphconfig={"ymin":N_words_pop_min}#,"ymax":entropycouples_old_norm_max}
custom_N_words_pop=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_words_ratio##########


def N_words_ratio(pop,**kwargs):
	words = set()
	n = 0
	for ag in pop._agentlist:
		for w in ag._vocabulary._content_decoding.keys():
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
custom_N_words_ratio=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########distance_used##########


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
custom_distance_used=custom_func.CustomFunc(FUNC,"population",**graphconfig)


#########discrim_success##########

def discrim_success(pop,**kwargs):
	n = 0
	for i in range(100):
		agent = random.choice(pop._agentlist)
		m1, m2 = agent._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2).next()
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
custom_discrim_success=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########discrim_success_semantic##########

def discrim_success_semantic(pop,**kwargs):
	n = 0
	for i in range(100):
		agent = random.choice(pop._agentlist)
		m1, m2 = agent._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2).next()
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
custom_discrim_success_semantic=custom_func.CustomFunc(FUNC,"population",**graphconfig)


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
	tempvalues=[]
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		tempm = np.linalg.matrix_rank(np.multiply(agent1.get_vocabulary_content(),agent2.get_vocabulary_content()))
		tempvalues.append(tempentropy(pop._M-tempm,pop._W-tempm))
	return np.mean(tempvalues)

def entropycouples_max(pop):
	return tempentropy(pop._M,pop._W)

def entropycouples_min(pop):
	return 0

FUNC=entropycouples
graphconfig={"ymin":entropycouples_min,"ymax":entropycouples_max}
custom_entropycouples=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropycouplesnorm##########


def entropycouples_norm(pop,**kwargs):
	return 1-(entropycouples(pop)/entropycouples_max(pop))

def entropycouples_norm_max(pop):
	return 1

def entropycouples_norm_min(pop):
	return 0

FUNC=entropycouples_norm
graphconfig={"ymin":entropycouples_norm_min,"ymax":entropycouples_norm_max}
custom_entropycouples_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########cat_agreement##########

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
			wl = [w for w,v in iv.data.items() if v == val_max]
			if wl:
				ivt1.setdefault(wl[0], IntervalTree()).add(Interval(iv.begin,iv.end))
		for iv in agent2._vocabulary._content_coding:
			val_max = max([0]+list(iv.data.values()))
			wl = [w for w,v in iv.data.items() if v == val_max]
			if wl:
				ivt2.setdefault(wl[0], IntervalTree()).add(Interval(iv.begin,iv.end))

		for w in ivt1.keys():
			ivt1[w].merge_overlaps()
		for w in ivt2.keys():
			ivt2[w].merge_overlaps()

		ivt = IntervalTree()
		for w in ivt1.keys():
			if w in ivt2.keys():
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
custom_cat_agreement=custom_func.CustomFunc(FUNC,"population",**graphconfig)

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

#########srtheo_cat##########
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
		ct = agent1._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2).next()
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
custom_srtheo_cat=custom_func.CustomFunc(FUNC,"population",**graphconfig)

###############""srtheo as used in epirob08 paper#############
def srtheo2(pop,**kwargs):
	C = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._M,pop._size))
	for ag in range(len(pop._agentlist)):
		for m in range(pop._M):
			try:
				best_scores[m,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_row(m))
			except TypeError:
				print 'e'
				print pop._agentlist[ag]._vocabulary.get_row(m)
				print max(pop._agentlist[ag]._vocabulary.get_row(m))
				print 'e'
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_row(m))
	n_meanings_used = 0
	for a in range(pop._size):
		for meaning in range(pop._M):
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
	D = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._W,pop._size))
	for ag in range(len(pop._agentlist)):
		for w in range(pop._W):
			try:
				best_scores[w,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_column(w))
			except TypeError:
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_column(w))
	for a in range(pop._size):
		for word in range(pop._W):
			score = best_scores[word,a]
			if score > 0:
				n_words_used += 1
				meanings = pop._agentlist[a]._vocabulary.get_known_meanings(w=word,option='max')
				if meanings:
					meaning = meanings[0]
					D[word,meaning] += 1.
	D = D/float(pop._size)
	n_words_used = n_words_used/float(pop._size)

	return sum(sum(np.multiply(C,D)))/float(pop._M)


def srtheo2_max(pop):
	return 1

def srtheo2_min(pop):
	return 0

FUNC=srtheo2
graphconfig={"ymin":srtheo2_min,"ymax":srtheo2_max}
custom_srtheo2=custom_func.CustomFunc(FUNC,"population",**graphconfig)

###############""srtheo as used in epirob08 paper#############
def srtheo3(pop,**kwargs):
	C = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._M,pop._size))
	for ag in range(len(pop._agentlist)):
		for m in range(pop._M):
			try:
				best_scores[m,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_row(m))
			except TypeError:
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_row(m))
	n_meanings_used = 0
	for a in range(pop._size):
		for meaning in range(pop._M):
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

	D = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._W,pop._size))
	for ag in range(len(pop._agentlist)):
		for w in range(pop._W):
			try:
				best_scores[w,ag] = np.amax(pop._agentlist[ag]._vocabulary.get_column(w))
			except TypeError:
				best_scores[m,ag] = max(pop._agentlist[ag]._vocabulary.get_column(w))
	n_words_used = 0
	for a in range(pop._size):
		for word in range(pop._W):
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

	return sum(sum(np.multiply(C,D)))/float(pop._M)


def srtheo3_max(pop):
	return 1

def srtheo3_min(pop):
	return 0

FUNC=srtheo3
graphconfig={"ymin":srtheo3_min,"ymax":srtheo3_max}
custom_srtheo3=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropydistrib##########

def entropydistrib(pop,**kwargs):
	tempmat=np.matrix(np.zeros((pop._M,pop._W)))
	for ag in pop._agentlist:
		tempmat=tempmat+ag._vocabulary.get_content()
	ans=0
	for m in range(pop._M):
		temp=pop._size
		for w in range(pop._W):
			temp=temp-tempmat[m,w]
		for w in range(pop._W):
			tempmat[m,w]=(tempmat[m,w]+temp/pop._W)/pop._size
			if tempmat[m,w]!=0:
				ans-=tempmat[m,w]*np.log2(tempmat[m,w])
	return ans

def entropydistrib_max(pop):
	return pop._M*np.log2(pop._W)

def entropydistrib_min(pop):
	return 0

FUNC=entropydistrib
graphconfig={"ymin":entropydistrib_min,"ymax":entropydistrib_max}
custom_entropydistrib=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########overlap##########

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
custom_overlap=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########overlap_semantic##########

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
			data1 = [w for w,v in iv.data.items() if v == val]
			if data != data1:
				ivt1.append(iv.begin)
				data = copy.copy(data1)
		ivt1.append(1.)
		ivt2 = []
		data = None
		for iv in sorted(ag2._vocabulary._content_coding):
			val = max([0]+list(iv.data.values()))
			data1 = [w for w,v in iv.data.items() if v == val]
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
custom_overlap_semantic=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########weight_over_degree##########

def weight_over_degree(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	values = []
	for ag in pop._agentlist:
		weight = 0
		for ed in G.edges(ag._id):
			weight += ed['weight']
		if weight != 0 :
			values.append(weight/G.degree(ag._id))
		else:
			values.append(0)
	return mean(values)

def weight_over_degree_max(pop):
	return 1

def weight_over_degree_min(pop):
	return 0


FUNC=weight_over_degree
graphconfig={"ymin":weight_over_degree_min,"ymax":weight_over_degree_max}
custom_weight_over_degree =custom_func.CustomFunc(FUNC,"population",**graphconfig)

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



#########max_mem##########

def max_mem(exp,X=0,**kwargs):

	mem = exp.db.get_graph(exp.uuid, method='Nlink')#mem = exp.graph(method='Nlink')
	return [max(mem._Y[0])]

def max_mem_min(exp):
	return 0

FUNC = max_mem

graphconfig = {"ymin":max_mem_min}#,"ymax":max_mem_max}
custom_max_mem =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_mem_conv##########

def max_mem_conv(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
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

	mem = exp.db.get_graph(exp.uuid, method='N_d')#mem = exp.graph(method='Nlink')
	return [max(mem._Y[0])]

def max_N_d_min(exp):
	return 0

FUNC = max_N_d

graphconfig = {"ymin":max_N_d_min}#,"ymax":max_N_d_max}
custom_max_N_d =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_N_d_conv##########

def max_N_d_conv(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
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
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
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

#########block_time##########

def block_time(exp,X=0,**kwargs):
	Nd_gr = exp.db.get_graph(exp.uuid, method='N_d')#exp.graph(method='srtheo')
	Nd = Nd_gr._Y[0]
	Nm_gr = exp.db.get_graph(exp.uuid, method='N_meanings')#exp.graph(method='srtheo')
	Nm = Nm_gr._Y[0]
	M = N_meanings_max(exp._poplist.get_last())
	for i in range(len(sr)):
		if Nm[i] == M and Nd == M:
			return [Nd_gr._X[0][i]]
	return [np.nan]

def block_time_max(exp):
	return exp._T[-1]

def block_time_min(exp):
	return 0

FUNC = block_time

graphconfig = {"ymin":block_time_min,"ymax":block_time_max}
custom_block_time =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########max_N_d_time##########

def max_N_d_time(exp,X=0,thresh=1.,**kwargs):
	N_d_gr = exp.db.get_graph(exp.uuid, method='N_d')#exp.graph(method='srtheo')
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

#########conv_time_plus_srtheo##########

def conv_time_plus_srtheo(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
	sr = sr_gr._Y[0]
	for i in range(len(sr)):
		if sr[i] >= thresh:
			break
	return [sr_gr._X[0][i]+(1.-sr_gr._Y[0][i])]


FUNC = conv_time_plus_srtheo

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time_plus_srtheo =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########partial_conv_time##########

def partial_conv_time(exp,X=0,thresh=1.,**kwargs):
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
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
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
	thresh = sr_gr._Y[0][-1]
	return max_mem(exp,X=X,thresh=thresh,**kwargs)


FUNC = max_mem_conv_threshold

graphconfig = {"ymin":max_mem_min}#,"ymax":max_mem_max}
custom_max_mem_conv_threshold = custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########conv_time_threshold##########

def conv_time_threshold(exp,X=0,**kwargs):
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
	thresh = sr_gr._Y[0][-1]
	return conv_time(exp,X=X,thresh=thresh,**kwargs)

FUNC = conv_time_threshold

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_conv_time_threshold =custom_func.CustomFunc(FUNC,"exp",**graphconfig)

#########partial_conv_time_threshold##########

def partial_conv_time_threshold(exp,X=0,**kwargs):
	sr_gr = exp.db.get_graph(exp.uuid, method='srtheo')#exp.graph(method='srtheo')
	thresh = sr_gr._Y[0][-1]
	return partial_conv_time(exp,X=X,thresh=thresh,**kwargs)


FUNC = partial_conv_time_threshold

graphconfig = {"ymin":conv_time_min,"ymax":conv_time_max}
custom_partial_conv_time_threshold = custom_func.CustomFunc(FUNC,"exp",**graphconfig)

################################################################




################  AUTRES    ####################################

def m_limit_theorique(M,W):
	return (-((M+W-1.)/2.)+math.sqrt((M+W-1.)**2/4.+2.*M*W))/2.

def decvec_from_MW(M,W):
	decvec=[]
	m=m_limit_theorique(M,W)
	for i in range(0,M+1):
		if i<=m:
			decvec.append(1)
		else:
			decvec.append(0)
	return decvec



def decvectest_from_MW(M,W):
	decvec=[]
	m0=0
	for i in range(0,M+1):
		dm=i-m0
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		print pp
		print pm
		print " "
		if pm<=pp:
			decvec.append(1)
		else:
			decvec.append(0)
	return decvec

def decvec2_from_MW(M,W):
	decvec=[]
	m0=0
	for i in range(0,M+1):
		dm=i-m0
		pp=(M-i)/float(M)*(W-i)/float(W-dm)
		pm=m0/float(M)*(m0-1.)/float(W-dm)
		print pp
		print pm
		print " "
		if pm<=pp:
			decvec.append(1)
			m0+=1
		else:
			decvec.append(0)
	return decvec


def decvec3_from_MW(M,W):
	decvec=[]
	for i in range(0,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		if pm*Gm<=pp*Gp:
			decvec.append(1)
		else:
			decvec.append(0)
	decvec.append(0)
	return decvec


def decvec3_softmax_from_MW(M,W,Temp):
	decvec=[]
	for i in range(0,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(-pm*Gm/Temp)
		decvec.append(P1/(P1+P2))
	decvec.append(0)
	return decvec


def decvec4_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P1/(P1+P2)
		if np.isnan(p):
			if pm*Gm<=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvec5_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(W-i)/float(W)
		pm=(i*(i-1)+(M-i)*(i-1))/float(M*W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P2/(P1+P2)
		if np.isnan(p):
			if pm*Gm>=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvectest_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(W-i)/float(W)
		pm=(i*(i-1)+(M-i)*(i-1))/float(M*W)
		Gp=np.log2(W-i)
		Gm=-np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P2/(P1+P2)
		if np.isnan(p):
			if pm*Gm>=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvec_full_explo(M,W):
	decvec = [1.]
	for i in range(1,M):
		decvec.append(1.)
	decvec.append(0.)


def decvec_full_teach(M,W):
	decvec = [1.]
	for i in range(1,M):
		decvec.append(0.)
	decvec.append(0.)

############################################################################
#NETWORKX TOOLS

def build_nx_graph(agent_list):
	G = nx.Graph()
	for ag in agent_list:
		tempm = np.sum(ag._vocabulary.get_content())
		G.add_node(ag._id,size=1.-(tempentropy(ag._M-tempm, ag._W-tempm)/tempentropy(ag._M, ag._W)))
	list_length = len(agent_list)
	for i in range(list_length):
		agent1 = agent_list[i]
		for j in range(i+1,list_length):
			agent2 = agent_list[j]
			tempmat = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
			tempm = np.sum(tempmat)
			weight = 1.-(tempentropy(agent1._M-tempm, agent1._W-tempm)/tempentropy(agent1._M, agent1._W))
			if weight != 0:
				G.add_edge(agent1._id,agent2._id,weight=weight)
	return G

def degree_distrib(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	return custom_graph.CustomGraph(nx.degree_histogram(G))

def edgevalue_distrib(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	dict_XY = {}
	for ed in G.edges:
		weight = ed['weight']
		if weight in dict_XY.keys():
			dict_XY[weight] += 1
		else:
			dict_XY[weight] = 1
	for key, value in dict_XY.items():
		X.append(key)
		Y.append(value)
	return custom_graph.CustomGraph(X=X,Y=Y)




#==================


def srtheo_voc(voc1,voc2=None,voc2_m=None,voc2_w=None,m=None,w=None,renorm=True,renorm_fact=None,role='both'):
	ans = 0.
	if role == 'both' or role == 'hearer':
		m1 = copy.deepcopy(voc1)
		if voc2 is not None:
			m2 = copy.deepcopy(voc2)
		else:
			m2 = copy.deepcopy(voc2_m)

		if m is not None:
			m2 = m2[m,:]
			m1 = m1[m,:]
		if w is not None:
			m1 = m1[:,w]
			m2 = m2[:,w]

		if renorm:
			if renorm_fact is None:
				m1 = m1 / np.linalg.norm(m1, axis=0, ord=1,keepdims=True)
				m2 = m2 / np.linalg.norm(m2, axis=1, ord=1,keepdims=True)
			else:
				m1 = m1 / renorm_fact
				m2 = m2 / renorm_fact
		mult = np.multiply(m1,m2)
		ans += 1./voc1.shape[0] * np.nan_to_num(mult).sum()
	if role == 'both' or role == 'speaker':
		m1 = copy.deepcopy(voc1)
		if voc2 is not None:
			m2 = copy.deepcopy(voc2)
		else:
			m2 = copy.deepcopy(voc2_w)

		if m is not None:
			m2 = m2[m,:]
			m1 = m1[m,:]
		if w is not None:
			m1 = m1[:,w]
			m2 = m2[:,w]

		if renorm:
			if renorm_fact is None:
				m1 = m1 / np.linalg.norm(m1, axis=1, ord=1,keepdims=True)
				m2 = m2 / np.linalg.norm(m2, axis=0, ord=1,keepdims=True)
			else:
				m1 = m1 / renorm_fact
				m2 = m2 / renorm_fact
		mult = np.multiply(m1,m2)
		ans += 1./voc1.shape[0] * np.nan_to_num(mult).sum()
	if role == 'both':
		return ans/2.
	else:
		return ans

#==================
