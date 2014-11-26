#!/usr/bin/python
# -*- coding: latin-1 -*-
import numpy as np
import random
import matplotlib.pyplot as plt
W=10 #nombre de words
M=10 # nombre de meanings
N=10 # nombre d'agents
T=10000#nb cycles

class agent:
	def __init__(self,Mp,Wp):
		self.memory=np.matrix(np.zeros((Mp,Wp)))
		self.M=Mp
		self.W=Wp
		self.I=0
	def affiche(self):
		print(self.memory)
	def pickm(self,*arg):
		if len(arg)==0:
			k=random.randint(0,self.M-1)
			return k
		knownmeanings=[]
		word=arg[0]
		for i in range(0,self.M):
			if self.memory[i,word]==1:
				knownmeanings.append(i)
		if len(knownmeanings)==0:
			k=random.randint(0,self.M-1)		
			return k
		else:
			return knownmeanings[random.randint(0,len(knownmeanings)-1)]	
	def pickw(self,meaning):
		knownwords=[]
		for i in range(0,self.W):
			if self.memory[meaning,i]==1:
				knownwords.append(i)
		if len(knownwords)==0:
			k=random.randint(0,self.W-1)
			return k
		else:
			return knownwords[random.randint(0,len(knownwords)-1)]
	def computeI(self):
		tempmu=[]
		tempw=[]
		testnonvide=0
		for i in range(0,self.M):
			tempw.append(0)
			for j in range(0,self.W):
				tempw[i]+=self.memory[i,j]
				testnonvide+=self.memory[i,j]
		for j in range(0,self.W):
			tempmu.append(0)
			for i in range(0,self.M):
				tempmu[j]+=self.memory[i,j]
		Itemp=0
		for i in range(0,self.M):
			for j in range(0,self.W):
				if self.memory[i,j]!=0:
					Itemp+=1.*self.memory[i,j]/tempw[i]*np.log2(1.*tempmu[j]/self.memory[i,j])
		I=np.log2(1./self.M)-1./self.M*Itemp
		self.I=I
class population:
 	def __init__(self,Np,Mp,Wp): 
 		self.agent=[]
 		for i in range(0,Np):
 			self.agent.append(agent(Mp,Wp))
 		self.size=Np
 		self.M=Mp
 		self.W=Wp
 	def addagent(self,Ap):
 		self.agent.append(Ap)
 		self.size+=1
 	def addnewagent(self):
 		self.agent.append(agent(self.M,self.W))
 		self.size+=1
 	def rmagent(self,Apn):
 		self.agent.remove(self.agent[Apn])
 		self.size-=1
 	def pickagent(self):
 		j=random.randint(0,self.size-1)
 		Ap=self.agent[j]#supposition forte sur la gestion de la memoire en python, a verifier
 		self.rmagent(j)
 		return Ap

data=[]
entropie=[]
pop=population(N,M,W)
for t in range(0,T):
	speaker=pop.pickagent()
	hearer=pop.pickagent()
	spM=speaker.pickm()
	spW=speaker.pickw(spM)
	hrM=hearer.pickm(spW)
	if hrM==spM:
		for j in range(0,W):
			if j==spW:
				hearer.memory[spM,j]=1
				speaker.memory[spM,j]=1
			else:
				hearer.memory[spM,j]=0
				speaker.memory[spM,j]=0
	else:
		hearer.memory[spM,spW]=1
		speaker.memory[spM,spW]=1
	hearer.computeI()
	speaker.computeI()
	pop.addagent(hearer)
	pop.addagent(speaker)

	print t
	#print "agent1"
	#pop.agent[0].affiche()
	#print "agent2"
	#pop.agent[1].affiche()
	Ndata=0
	Sdata=0
	for n in range(0,N):
		for j in range(0,W):
			for i in range(0,M):
				Ndata+=pop.agent[n].memory[i,j]
		Sdata+=pop.agent[n].I
	data.append(Ndata/(N*1.))
	entropie.append(Sdata)
plt.plot(entropie)
plt.show()
