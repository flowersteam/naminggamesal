#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngsimu import *
import numpy as np
import custom_func

def pop_ize(func):
	def out_func(pop,*progress_info):
		tempNlist=[]
		agentlist=pop._agentlist
		for i in range(0,len(agentlist)):
			if len(progress_info)!=0:
				progress_info=progress_info[0]+" numagent:"+str(i)+"/"+str(pop._size)
				tempNlist.append(func(agentlist[i],progress_info))
			else:
				tempNlist.append(func(agentlist[i]))
			mean=np.mean(tempNlist)
			std=np.std(tempNlist)
		return [mean,std,tempNlist]
	out_func.__name__=func.__name__+"_moyen"
	return out_func

def Nlinkmoyenpop(pop,*progress_info):
	tempNlist=[]
	agentlist=pop._agentlist
	for i in range(0,len(agentlist)):
		tempN=0
		for m in range(0,pop._M):
			for w in range(0,pop._W):
				if len(progress_info)!=0:
					print progress_info[0]+"m:"+str(m)+"/"+str(pop._M)+" w:"+str(w)+"/"+str(pop._W)+" numagent:"+str(i)+"/"+str(pop._size)
				tempN+=agentlist[i]._vocabulary.exists(m,w)
		tempNlist.append(tempN)
		mean=np.mean(tempNlist)
		std=np.std(tempNlist)
	return [mean,std,tempNlist]


custom_Nlinkmoyenpop=custom_func.CustomFunc(Nlinkmoyenpop,"agent")



############################	LEVEL AGENT ############################

#### 	INPUT:		 agent , *progress_info
####	OUTPUT:		[mean,std,(tempNlist)]

#	FUNC_BIS=pop_ize(FUNC)
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"agent")

def Nlink(agent,*progress_info):
	tempN=0
	for m in range(0,agent._M):
		for w in range(0,agent._W):
			if len(progress_info)!=0:
				print progress_info[0]+"m:"+str(m)+"/"+str(agent._M)+" w:"+str(w)+"/"+str(agent._W)
			tempN+=agent._vocabulary.exists(m,w)
	return tempN

FUNC=Nlink
FUNC_BIS=pop_ize(FUNC)
custom_Nlink =custom_func.CustomFunc(FUNC_BIS,"agent")



def success_rate(agent,*progress_info):
	if len(progress_info)!=0:
		print progress_info[0]
	if agent.success+agent.fail!=0:
		return agent.success/float(agent.success+agent.fail)
	else:
		return 0

FUNC=success_rate
FUNC_BIS=pop_ize(FUNC)
custom_success_rate=custom_func.CustomFunc(FUNC_BIS,"agent")

############################	LEVEL POPULATION ############################

#### 	INPUT:		 pop, *progress_info
####	OUTPUT:		value

#	custom_FUNC=custom_func.CustomFunc(FUNC,"population")


def Nlinksurs(pop,*progress_info):
	tempmat=np.matrix(np.ones((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat=np.multiply(tempmat,agent._vocabulary.get_content())
	return np.sum(tempmat)

FUNC=Nlinksurs
custom_Nlinksurs=custom_func.CustomFunc(FUNC,"population")

############################	LEVEL EXPE ############################

#### 	INPUT:		 expe, *progress_info
####	OUTPUT:		[value,(opt)]

#	custom_FUNC=custom_func.CustomFunc(FUNC,"experiment")
