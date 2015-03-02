#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngsimu import *
import numpy as np
import math
import custom_func
import my_functions

def pop_ize(func):
	def out_func(pop,**kwargs):
		tempNlist=[]
		agentlist=pop._agentlist
		for i in range(0,len(agentlist)):
			if "progress_info" in kwargs.keys():
				progress_info=kwargs["progress_info"]+" numagent:"+str(i)+"/"+str(pop._size)
				tempNlist.append(func(agentlist[i],progress_info=progress_info))
			else:
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
			if "progress_info" in kwargs.keys():
				progr_info=kwargs["progress_info"]+" m:"+str(m)+"/"+str(agent._M)+" w:"+str(w)+"/"+str(agent._W)
				my_functions.print_on_line_pid(progr_info)
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
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
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
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
	m=len(agent._vocabulary.get_known_meanings())
	return tempentropy(agent._M-m,agent._W-m)

def entropy_max(pop):
	return tempentropy(pop._M,pop._W)

def entropy_min(pop):
	return 0

FUNC=entropy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":entropy_min,"ymax":entropy_max}
custom_entropy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

############################	LEVEL POPULATION ############################

#### 	INPUT:		pop, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs##########

def Nlinksurs(pop,**kwargs):
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
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
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
	m=Nlinksurs(pop)
	return tempentropy(pop._M-m,pop._W-m)

def entropypop_max(pop):
	return tempentropy(pop._M,pop._W)

def entropypop_min(pop):
	return 0

FUNC=entropypop
graphconfig={"ymin":entropypop_min,"ymax":entropypop_max}
custom_entropypop=custom_func.CustomFunc(FUNC,"population",**graphconfig)


#########entropycouples##########

def entropycouples(pop,**kwargs):
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
	tempvalues=[]
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		tempmat=np.multiply(agent1._vocabulary.get_content(),agent2._vocabulary.get_content())
		m=np.sum(tempmat)
		tempvalues.append(tempentropy(pop._M-m,pop._W-m))
	return np.mean(tempvalues)

def entropycouples_max(pop):
	return tempentropy(pop._M,pop._W)

def entropycouples_min(pop):
	return 0

FUNC=entropycouples
graphconfig={"ymin":entropycouples_min,"ymax":entropycouples_max}
custom_entropycouples=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropydistrib##########

def entropydistrib(pop,**kwargs):
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
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