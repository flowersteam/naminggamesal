#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngsimu import *
import numpy as np
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
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"agent")

def Nlink(agent,**kwargs):
	tempN=0
	for m in range(0,agent._M):
		for w in range(0,agent._W):
			if "progress_info" in kwargs.keys():
				progr_info=kwargs["progress_info"]+" m:"+str(m)+"/"+str(agent._M)+" w:"+str(w)+"/"+str(agent._W)
				my_functions.print_on_line_pid(progr_info)
			tempN+=agent._vocabulary.exists(m,w)
	return tempN

FUNC=Nlink
FUNC_BIS=pop_ize(FUNC)
custom_Nlink =custom_func.CustomFunc(FUNC_BIS,"agent")



def success_rate(agent,**kwargs):
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
	if agent.success+agent.fail!=0:
		return agent.success/float(agent.success+agent.fail)
	else:
		return 0

FUNC=success_rate
FUNC_BIS=pop_ize(FUNC)
custom_success_rate=custom_func.CustomFunc(FUNC_BIS,"agent")

############################	LEVEL POPULATION ############################

#### 	INPUT:		pop, **progress_info
####	OUTPUT:		value

#	custom_FUNC=custom_func.CustomFunc(FUNC,"population")


def Nlinksurs(pop,**kwargs):
	if "progress_info" in kwargs.keys():
		my_functions.print_on_line_pid(kwargs["progress_info"])
	tempmat=np.matrix(np.ones((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat=np.multiply(tempmat,agent._vocabulary.get_content())
	return np.sum(tempmat)

FUNC=Nlinksurs
custom_Nlinksurs=custom_func.CustomFunc(FUNC,"population")

############################	LEVEL EXPE ############################

#### 	INPUT:		expe, **progress_info
####	OUTPUT:		value

#	custom_FUNC=custom_func.CustomFunc(FUNC,"experiment")

