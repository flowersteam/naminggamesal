#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
from scipy import sparse

class vocabulary:
	def affiche(self):
		print(self.content)



class vocsparse(vocabulary):
	typevoc="sparse"
	def __init__(self,M,W):
		self.M=M
		self.W=W
		self.size=[M,W]
		self.content=sparse.lil_matrix((M,W))

class vocmatrix(vocabulary):
#	typevoc="matrix"
	def __init__(self,M,W):
		self.M=M
		self.W=W
		self.size=[M,W]
		self.content=np.matrix(np.zeros((self.M,self.W)))
		

test=vocmatrix(3,4)
print test.M
print test.content
