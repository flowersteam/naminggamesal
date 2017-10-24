#!/usr/bin/python

import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module
import copy

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
	'matrix_new':'matrix_new.VocMatrixNew'
}



def voc_cache(tempfun):
	def mod_fun(obj_self, *args, **kwargs):
		#ans = tempfun(obj_self, *args, **kwargs)
		#return ans
		args_list = sorted([str(val) for val in list(args) + list(kwargs.values())])
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
	if tempstr in list(voc_class.keys()):
		tempstr = voc_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	try:
		_tempmod = import_module('.'+temppath,package=__name__)
	except (KeyError,AttributeError):
		raise ImportError('No such class: '+str(temppath)+'.'+str(tempclass))
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




class BaseVocabularyElaborated(BaseVocabulary):


	def __init__(self, start='empty', **voc_cfg2):
		#self._M = M
		#self._W = W
		self.unknown_meanings = []
		self.unknown_words = []
		self.accessible_meanings = []
		self.accessible_words = []
		#if valmax1:
		#	self.valmax = 1.
		#self._size = [self._M,self._W]
		#M = voc_cfg2['M']
		#W = voc_cfg2['W']
		BaseVocabulary.__init__(self,**voc_cfg2)

		self._content_m = self.init_empty_content()
		self._content_w = self.init_empty_content()

		if start == 'completed':
			self.complete_empty()

	def fill(self):
		for m in self.get_accessible_meanings():
			for w in self.get_accessible_words():
				self.add(m,w)

	def init_empty_content(self,option='m'):
		return {}

	@del_cache
	def complete_empty(self):
		assert len(self.get_known_meanings()) == 0
		print("complete_empty not implemented yet")

	@del_cache
	def empty(self):
		m_list = self.get_accessible_meanings()
		w_list = self.get_accessible_words()
		self._content_m = self.init_empty_content()
		self._content_w = self.init_empty_content()
		self.unknown_meanings = m_list
		self.unknown_words = w_list

	@voc_cache
	def exists(self,m,w):
		if self.get_value(m,w,content_type='m') > 0 or self.get_value(m,w,content_type='w') > 0:
			return 1
		else:
			return 0



	def __eq__(self,other):
		if isinstance(other, self.__class__):
			if set(self.get_known_words()) != set(other.get_known_words()):
				return False
			else:
				for w in self.get_known_words():
					if set(self.get_known_meanings(w=w)) != set(other.get_known_meanings(w=w)):
						return False
			if set(self.get_known_meanings()) != set(other.get_known_meanings()):
				return False
			else:
				for m in self.get_known_meanings():
					if set(self.get_known_words(m=m)) != set(other.get_known_words(m=m)):
						return False
			return True
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def get_content(self,content_type='m'):
		if content_type == 'm':
			return self._content_m
		elif content_type == 'w':
			return self._content_w
		else:
			raise ValueError('unknown content type:'+str(content_type))

	@voc_cache
	def get_size(self):
		return [self.get_M(),self.get_W()]
		#return [len(self.get_accessible_meanings()),len(self.get_accessible_words())]



	def add_value(self,m,w,val=1,context=[],content_type='both'):
		if content_type in ['m','both']:
			val_init = self.get_value(m,w,content_type='m')
			val_fin = max(0,val_init+val)
			self.add(m,w,val_fin,content_type='m')
		if content_type in ['w','both']:
			val_init = self.get_value(m,w,content_type='w')
			val_fin = max(0,val_init+val)
			self.add(m,w,val_fin,content_type='w')

	def multiply_value(self,m,w,val=1,context=[],content_type='both'):
		if content_type in ['m','both']:
			val_init = self.get_value(m,w,content_type='m')
			val_fin = max(0,val_init*val)
			self.add(m,w,val_fin,content_type='m')
		if content_type in ['w','both']:
			val_init = self.get_value(m,w,content_type='w')
			val_fin = max(0,val_init*val)
			self.add(m,w,val_fin,content_type='w')

	def diagnostic(self):
		print(self._cache)
		print(self)

	def get_random_known_m(self,w=None, option='max'):
		if not len(self.get_known_meanings(w=w)) == 0:
			m = random.choice(self.get_known_meanings(w=w, option=option))
		else:
			#print "tried to get known m but none are known"
			m = self.get_new_unknown_m()
		return m

	def get_random_known_w(self,m=None, option='max'):
		if not len(self.get_known_words(m=m)) == 0:
			w = random.choice(self.get_known_words(m=m, option=option))
		else:
			#print "tried to get known w but none are known"
			w = self.get_new_unknown_w()
		return w


	#@voc_cache
	def get_accessible_meanings(self):
		l = copy.deepcopy(self.accessible_meanings)#list(self.get_known_meanings())+list(self.unknown_meanings)
		try:
			return sorted(l)
		except:
			return l

	#@voc_cache
	def get_accessible_words(self):
		l = copy.deepcopy(self.accessible_words)#list(self.get_known_words())+list(self.unknown_words)
		try:
			return sorted(l)
		except:
			return l

	def get_random_m(self):
		return random.choice(self.get_accessible_meanings()) #random from known+explored+adjacent_possible

	def get_new_unknown_m(self):
		if len(self.unknown_meanings) != 0:
			m = random.choice(self.unknown_meanings)
		else:
			#print "tried to get new m but all are known"
			m = self.get_random_known_m()
		return m

	def get_new_unknown_w(self):
		if hasattr(self,'next_word'):
			w = self.next_word
			delattr(self,'next_word')
		elif len(self.unknown_words) != 0:
			w = random.choice(self.unknown_words)
		else:
			#print "tried to get new w but all are known"
			w = self.get_random_known_w()
		return w


	@del_cache
	def discover_meanings(self,m_list):
		#m_list = list(set(list(m_list)))
		m_list = [ii for n,ii in enumerate(m_list) if ii not in m_list[:n]]
		m_list_bis = [m for m in m_list if m not in self.accessible_meanings]#known_meanings()+self.unknown_meanings]
		self.unknown_meanings += m_list_bis
		self.accessible_meanings += m_list_bis
		return m_list_bis

	@del_cache
	def discover_words(self,w_list):
		#w_list = list(set(list(w_list)))
		w_list = [ii for n,ii in enumerate(w_list) if ii not in w_list[:n]]
		w_list_bis = [w for w in w_list if w not in self.accessible_words]#known_words()+self.unknown_words]
		self.unknown_words += w_list_bis
		self.accessible_words += w_list_bis
		return w_list_bis

	def get_unknown_meanings(self):
		try:
			list.sort(self.unknown_meanings)
		except:
			pass
		return self.unknown_meanings

	def get_unknown_words(self):
		try:
			list.sort(self.unknown_words)
		except:
			pass
		return self.unknown_words


	def get_M(self):
		return self.get_UM()+self.get_KM()

	def get_W(self):
		return self.get_UW()+self.get_KW()

	def get_UM(self):
		return len(self.unknown_meanings)

	def get_UW(self):
		return len(self.unknown_words)





	def init_empty_content(self,option='m'):
		return {}

	def get_KM(self):
		return len(self._content_m)

	def get_KW(self):
		return len(self._content_w)

	def get_alterable_shallow_copy(self):
		return copy.deepcopy(self)
		#return AlterableShallowCopyVoc2DictDict(voc=self)

	#def inherit_from: to split a meaning or a word

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		pass

	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		pass


	#@voc_cache
	def get_known_meanings_weights(self,w):
		pass

	#@voc_cache
	def get_known_words_weights(self,m):
		pass

	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		pass

	#@voc_cache
	def get_known_words_weights_values(self,m):
		pass

	#@voc_cache
	def get_known_meanings_weights_indexes(self,w):
		pass

	#@voc_cache
	def get_known_words_weights_indexes(self,m):
		pass

	@del_cache
	def add(self,m,w,val=1,context=[],content_type='both'):
		pass

	@del_cache
	def rm(self,m,w,content_type='both'):
		pass

	def get_value(self,m,w,content_type='m'):
		pass

	def rm_syn(self,m,w,content_type='both'):
		for i in self.get_known_words(m=m):
			if i!=w:
				self.rm(m,i,content_type=content_type)

	def rm_hom(self,m,w,content_type='both'):
		for i in self.get_known_meanings(w=w):
			if i!=m:
				self.rm(i,w,content_type=content_type)
