#!/usr/bin/python
# -*- coding: latin-1 -*-

#Strategie "on efface tout" ni synonyme ni homonyme possible


import numpy as np
import math
import random
import matplotlib.pyplot as plt
import copy as cp
W=20 #nombre de words
M=20 # nombre de meanings
N=10 # nombre d'agents
T=10000#nb cycles

class agent:
	def __init__(self,Mp,Wp):
		self.memory=np.matrix(np.zeros((Mp,Wp)))
		self.knownmeanings=np.zeros(Mp)
		self.knownwords=np.zeros(Wp)
		self.M=Mp
		self.W=Wp

	def pickneww(self):
		temp=self.W-sum(self.knownwords)
		if temp==0:
			w=random.randint(0,self.W-1)
		else:
			temp2=random.randint(1,temp)
   			w=-1
   			i=0
			while i<temp2 :
				w+=1
				if self.knownwords[w]==0:
					i+=1
		return w




	def pickmw(self): #on pick au hasard complet un m ; w s il y en a un associé, sinon random 
		m=random.randint(0,self.M-1)
		if self.knownmeanings[m]==0:
			w=self.pickneww()
		else:
			for i in range(0,self.W):
				if self.memory[m,i]==1:
					w=i
		return([m,w])

	def update(self):
		for i in range(0,self.M):
			self.knownmeanings[i]=0
		for j in range(0,self.W):
			self.knownwords[j]=0
		for i in range(0,self.M):
			for j in range(0,self.W):
				if self.memory[i,j]!=0:
					self.knownmeanings[i]=1
					self.knownwords[j]=1

	def insert(self,coord): #on insere un 1 en m w en virant tous les syn et hom
		m=coord[0]
		w=coord[1]
		for i in range(0,self.M):
			if i!=m:
				self.memory[i,w]=0
		for i in range(0,self.W):
			if i!=w:
				self.memory[m,i]=0
		self.memory[m,w]=1
		self.update()

	def affiche(self):
		print(self.memory)



class population:
 	def __init__(self,Np,Mp,Wp): 
 		self.agent=[]
 		for i in range(0,Np):
 			self.agent.append(agent(Mp,Wp))
 		self.size=Np
 		self.M=Mp
 		self.W=Wp
 		self.update()
 	def update(self):
 		temp=np.matrix(np.zeros((self.M,self.W)))
 		temp2=np.matrix(np.ones((self.M,self.W)))
 		for i in range(0,self.size):
 			temp+=self.agent[i].memory
 			temp2=np.multiply(temp2,self.agent[i].memory)
 		self.view1=temp/(self.size*1.)
 		self.view2=temp2
 	def addagent(self,Ap):
 		self.agent.append(Ap)
 		self.size+=1
 		self.update()
 	def addnewagent(self):
 		self.agent.append(agent(self.M,self.W))
 		self.size+=1
 		self.update()
 	def rmagent(self,Apn):
 		self.agent.remove(self.agent[Apn])
 		self.size-=1
 		self.update()
 	def pickagent(self):
 		j=random.randint(0,self.size-1)
 		Ap=cp.deepcopy(self.agent[j])
 		self.rmagent(j)
 		return Ap
 	def affiche(self):
 		print self.view1 






data=[]
S=[]
Spop=[]
pop=population(N,M,W)
for t in range(0,T):
	speaker=pop.pickagent()
	hearer=pop.pickagent()
	tempcoord=speaker.pickmw()
	speaker.insert(tempcoord)
	hearer.insert(tempcoord)
	pop.addagent(hearer)
	pop.addagent(speaker)

	print t
	Ndata=0
	Nagent=0
	Sdata=0
	for n in range(0,N):
		Nagent=0
		for j in range(0,W):
			for i in range(0,M):
				Nagent+=pop.agent[n].memory[i,j]
		if M!=Nagent:
			Sdata+=np.log2(math.factorial(M-Nagent))
		Ndata+=Nagent
	Npop=0
	for j in range(0,W):
			for i in range(0,M):
				Npop+=pop.view2[i,j]
	print Npop
	Spop.append(np.log2(math.factorial(M-Npop)))
	data.append(Ndata/(N*1.))
	S.append(Sdata/(N*1.))
pop.affiche()
plt.plot(S)
plt.title("S moyen par agent")
plt.show()
plt.plot(data)
plt.title("nombre d'associations moyen par agent")
plt.show()
plt.plot(Spop)
plt.title("S population")
plt.show()


############## le choix de m w devrait prendre en compte les w deja pris
############### Pour l instant on considere uniquement M=W