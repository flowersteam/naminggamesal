#!/usr/bin/python
# -*- coding: latin-1 -*-
#####################################"" MATRICES CREUSES #############################################

from .matrix import VocMatrix
from scipy import sparse
import numpy as np

class VocSparseMatrix(VocMatrix):
	voctype="sparse_matrix"

	def __init__(self,M,W,**voc_cfg2):
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._M = M
		self._W = W
		self._content=sparse.lil_matrix((self._M,self._W),dtype=np.float16)

	def get_content(self):
		return self._content.todense()
