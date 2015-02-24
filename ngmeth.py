#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngsimu import *
import numpy as np

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

def Nlinkmoyenexpe(expe,*progress_info):
	poplist=expe._poplist
	tmpNlist=[]
	tmpstdlist=[]
	for i in range(0,len(poplist)):
		print "T:"+str(i)
		tempdata=Nlinkmoyenpop(poplist[i])
		tmpNlist.append(tempdata[0])
		tmpstdlist.append(tempdata[1])
	return [tmpNlist,tmpstdlist]
	

#import matplotlib.pyplot as plt

#data=ngmeth.Nlinkmoyenexpe(testexp)




