#!/usr/bin/python
import numpy as np
import math

import additional.custom_func as custom_func
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
	out_func.__name__=func.__name__+"_moyen"
	return out_func



############################	LEVEL AGENT ############################

#### 	INPUT:		agent , **progress_info
####	OUTPUT:		[mean,std,(tempNlist)]

#	FUNC_BIS=pop_ize(FUNC)
#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Nlink##########

def Nlink(agent,**kwargs):
	tempN=0
	for m in range(0,agent._M):
		for w in range(0,agent._W):
			tempN+=agent._vocabulary.exists(m,w)
	return tempN

def Nlink_max(pop):
	return pop._M

def Nlink_min(pop):
	return 0


FUNC=Nlink
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Nlink_min,"ymax":Nlink_max}
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

#########Nlinksurs##########

def Nlinksurs(pop,**kwargs):
	tempmat=np.matrix(np.ones((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat=np.multiply(tempmat,agent._vocabulary.get_content())
	return np.sum(tempmat)

def Nlinksurs_max(pop):
	return pop._M

def Nlinksurs_min(pop):
	return 0

FUNC=Nlinksurs
graphconfig={"ymin":Nlinksurs_min,"ymax":Nlinksurs_max}
custom_Nlinksurs=custom_func.CustomFunc(FUNC,"population",**graphconfig)


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


#########entropycouples##########

def entropycouples(pop,**kwargs):
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

#########srtheo##########

def srtheo(pop,**kwargs):
	fail=0
	succ=0
	for i in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		pop_cfg={
			'voc_cfg':{
			'voc_type':'sparse_matrix',
			    'M':pop._M,
			    'W':pop._W
			    },
			'strat_cfg':{
			    'strat_type':'naive'
			    },
			'interact_cfg':{
			    'interact_type':'speakerschoice'
			    },
			'nbagent':2
			}
		tempop=Population(**pop_cfg)
		tempop._agentlist[0]._vocabulary._content=agent1._vocabulary.get_content()
		tempop._agentlist[1]._vocabulary._content=agent2._vocabulary.get_content()
		tempop.play_game(1)
		if tempop._lastgameinfo[0]==tempop._lastgameinfo[2]:
			succ+=1
		else:
			fail+=1
	return succ/float(succ+fail)

def srtheo_max(pop):
	return 1

def srtheo_min(pop):
	return 0

FUNC=srtheo
graphconfig={"ymin":srtheo_min,"ymax":srtheo_max}
custom_srtheo=custom_func.CustomFunc(FUNC,"population",**graphconfig)

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


############################	LEVEL EXPE ############################

#### 	INPUT:		expe, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"experiment",**graphconfig)




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
