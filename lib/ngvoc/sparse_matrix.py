#!/usr/bin/python
# -*- coding: latin-1 -*-
#####################################"" MATRICES CREUSES #############################################

from . import *
from scipy import sparse

class VocSparseMatrix(VocMatrix):
	voctype="sparse_matrix"
	
	def __init__(self,M,W):
		super(VocMatrix,self).__init__(M,W)
		self._content=sparse.lil_matrix((M,W),dtype=np.float16)

	def get_content(self):
		return self._content.todense()