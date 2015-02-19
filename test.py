#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
from scipy import sparse

class vocabulary:
	def affiche(self):
		print(self.typevoc)



class vocsparse(vocabulary):
	typevoc="sparse"
	def sparse(self,M):
		return M*M

class vocmatrix(vocabulary):
	typevoc="matrix"
	def mat(self,W):
		return W
