#!/usr/bin/python
# -*- coding: latin-1 -*-
import numpy as np
import random
W=5 #nombre de words
M=8 # nombre de meanings
N=10 # nombre d'agents

class agent:
	def __init__(self):
		self.memory=np.matrix(np.zeros((W,M)))
	def affiche(self):
		print(self.memory)
	def pickm(self):
		return random.randint(0,M-1)
	def pickw(self,meaning):
		knownwords=[]
		for i in range(0,W-1):
			if self.memory[i,meaning]==1:
				knownwords.append(i)
		return knownwords[random.randint(0,len(knownwords)-1)]		

# class population:
# 	def addagent
# 	def rmagent
# 	def init 
# 	# initialiser la population (taille, autres?)
# 	def pickagent

agent1=agent()
for i in range(0,M):
	print i
	agent1.memory[3,i]=1
	agent1.memory[4,i]=1
agent1.affiche()
x=agent1.pickm()
print x
test=agent1.pickw(x)
print(test)