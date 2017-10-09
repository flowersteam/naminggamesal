#!/usr/bin/python

import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

sns.set(rc={'image.cmap': 'Purples_r'})

#####Base class

voc_class={
	"matrix":"matrix.VocMatrix",
	"lil_matrix":"matrix.VocLiLMatrix",
	"csr_matrix":"matrix.VocCSRMatrix",
	"csr_matrix_improved":"matrix.VocCSRMatrixImproved",
	"csc_matrix":"matrix.VocCSCMatrix",
	"dok_matrix":"matrix.VocDOKMatrix",
	"graph":"graph.VocGraph",
	"graph_ba":"graph.BarabasiAlbertVocGraph",
	'category':'category.VocCategory',
	'2dictdict':'twodictdict.Voc2DictDict',
	'pandas':'pd_df.VocPandas',
}



def voc_cache(tempfun):
	def mod_fun(obj_self, *args, **kwargs):
		#ans = tempfun(obj_self, *args, **kwargs)
		#return ans
		args_list = sorted([str(val) for val in list(args) + kwargs.values()])
		args_str = ''.join(args_list)
		try:
			return obj_self._cache[tempfun.__name__+args_str]
		except KeyError:
			obj_self._cache[tempfun.__name__+args_str] = tempfun(obj_self, *args, **kwargs)
			return obj_self._cache[tempfun.__name__+args_str]
	return mod_fun

def del_cache(tempfun):
	def mod_fun_del(obj_self, *args, **kwargs):
		ans = tempfun(obj_self, *args, **kwargs)
		obj_self._cache = {}
		return ans
	return mod_fun_del

def get_vocabulary(voc_type='matrix', **voc_cfg2):
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

	def __str__(self):
		str1 = 'Words\n'
		str2 = 'Meanings'
		content = str(self.get_content()).split('\n')
		x = len(content[0])
		y = len(content)
		str1 = (len(str2)+max(0,(x-len(str1))/2))*" "+str1
		indice = y/2
		str2_list = [" "*len(str2)]*indice+[str2]+[" "*len(str2)]*(y-indice-1)
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

	@del_cache
	def del_cache(self):
		pass

	def finish_update(self):
		self.del_cache()

	#@del_cache
	def discover_meanings(self,m_list):
		pass

	#@del_cache
	def discover_words(self,w_list):
		pass

	def get_accessible_meanings(self):
		return self.get_known_meanings()+self.get_unknown_meanings()
	
	def get_accessible_words(self):
		return self.get_known_words()+self.get_unknown_words()

