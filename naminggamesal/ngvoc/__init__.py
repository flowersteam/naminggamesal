#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base

voc_class={
	"matrix":"matrix.VocMatrix",
	"sparse_matrix":"matrix.VocSparseMatrix"
}



def voc_cache(tempfun):
	def mod_fun(self, *args):
		try:
			return self._cache[tempfun.__name__+str(args)]
		except KeyError:
			self._cache[tempfun.__name__+str(args)] = tempfun(self, *args)
			return self._cache[tempfun.__name__+str(args)]
	return mod_fun

def del_cache(tempfun):
	def mod_fun(obj_self, *args):
		ans = tempfun(obj_self, *args)
		obj_self._cache={}
		return ans
	return mod_fun

def Vocabulary(voc_type='matrix', **voc_cfg2):
	tempstr = voc_type
	if tempstr in voc_class.keys():
		tempstr = voc_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	tempvoc = getattr(_tempmod,tempclass)(**voc_cfg2)
	return tempvoc


class BaseVocabulary(object):

	def __init__(self,**voc_cfg2):
		self._cache = {}

	@del_cache
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


###### Classes supplémentaires

#from .matrix import *
#from .sparse_matrix import *