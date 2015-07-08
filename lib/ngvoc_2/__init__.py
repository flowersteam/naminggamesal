#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base

class Vocabulary(object):

	def __init__(self,M,W):
		self._M=M
		self._W=W
		self._size=[M,W]

	def fill(self):
		for i in range(0,self._M):
			for j in range(0,self._W):
				self.add(i,j,1)

	def __str__(self):
		str1 = 'Words\n'
		str2 = 'Meanings'
		content = str(self.get_content()).split('\n')
		x=len(content[0])
		y=len(content)
		str1= (len(str2)+max(0,(x-len(str1))/2))*" "+str1
		indice=y/2
		str2_list=[" "*len(str2)]*indice+[str2]+[" "*len(str2)]*(y-indice-1)
		for i in range(y):
			str1 += str2_list[i]
			str1 += content[i]+"\n"
		return str1

	def get_voctype(self):
		return _voctype

	def get_M(self):
		return self._M

	def get_W(self):
		return self._W


###### Classe supplémentaires

from .matrix import *
from .sparse_matrix import *

voc_class={
	"matrix":VocMatrix,
	"sparse_matrix":VocSparseMatrix
}
