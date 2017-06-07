#!/usr/bin/python

import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import scipy
from scipy import sparse

from . import BaseVocabulary
from . import voc_cache, del_cache




class Voc2DictDict(BaseVocabulary):

	def __init__(self, start='empty',**voc_cfg2):
		#self._M = M
		#self._W = W
		self.unknown_meanings = []
		self.unknown_words = []
		#self._size = [self._M,self._W]
		#M = voc_cfg2['M']
		#W = voc_cfg2['W']
		BaseVocabulary.__init__(self,**voc_cfg2)
		self._content_m = {}
		self._content_w = {}

		if start == 'completed':
			self.complete_empty()

	#@del_cache
	def complete_empty(self):
		assert len(self.get_known_meanings()) == 0
		print "complete_empty not implemented yet"

	#@del_cache
	def empty(self):
		m_list = self.get_accessible_meanings()
		w_list = self.get_accessible_words()
		self.content_m = {}
		self.content_w = {}
		self.unknown_meanings = m_list
		self.unknown_words = w_list

	#@voc_cache
	def exists(self,m,w):
		if self.get_value(m,w,content_type='m') > 0 or self.get_value(m,w,content_type='w') > 0:
			return 1
		else:
			return 0

	def get_value(self,m,w,content_type='m'):
		try:
			if content_type == 'm':
				return self._content_m[m][w]
			elif content_type == 'w':
				return self._content_w[w][m]
			else:
				raise ValueError('unknown content type:'+str(content_type))
		except KeyError:
			return 0

	def get_content(self,content_type='m'):
		if content_type == 'm':
			return self._content_m
		elif content_type == 'w':
			return self._content_w
		else:
			raise ValueError('unknown content type:'+str(content_type))

	#@voc_cache
	def get_size(self):
		return [self.get_M(),self.get_W()]
		#return [len(self.get_accessible_meanings()),len(self.get_accessible_words())]


	#@del_cache
	def add(self,m,w,val=1,context=[],content_type='both'):
		if val <= 0:
			self.rm(m,w,content_type=content_type)
		else:
			if content_type == 'm':
				if m not in self._content_m.keys():#self.get_known_meanings():
					self._content_m[m] = {}
				self._content_m[m][w] = val
				if m in self.unknown_meanings:
					self.unknown_meanings.remove(m)
				if w in self.unknown_words:
					self.unknown_words.remove(w)
			elif content_type == 'w':
				if w not in self._content_w.keys():#self.get_known_words():
					self._content_w[w] = {}
				self._content_w[w][m] = val
				if m in self.unknown_meanings:
					self.unknown_meanings.remove(m)
				if w in self.unknown_words:
					self.unknown_words.remove(w)
			elif content_type == 'both':
				self.add(m=m,w=w,val=val,context=context,content_type='m')
				self.add(m=m,w=w,val=val,context=context,content_type='w')
			else:
				raise ValueError('unknown content type:'+str(content_type))


	def add_value(self,m,w,val=1,context=[],content_type='both'):
		if content_type in ['m','both']:
			val_init = self.get_value(m,w,content_type='m')
			val_fin = max(0,val_init+val)
			self.add(m,w,val_fin,content_type='m')
		if content_type in ['w','both']:
			val_init = self.get_value(m,w,content_type='w')
			val_fin = max(0,val_init+val)
			self.add(m,w,val_fin,content_type='w')

	#@del_cache
	def rm(self,m,w,content_type='both'):
		if content_type == 'm':
			if m in self._content_m.keys() and w in self._content_m[m].keys():
				del self._content_m[m][w]
				if self._content_m[m] == {}:
					del self._content_m[m]
					self.unknown_meanings.append(m)
		elif content_type == 'w':
			if w in self._content_w.keys() and m in self._content_w[w].keys():
				del self._content_w[w][m]
				if self._content_w[w] == {}:
					del self._content_w[w]
					self.unknown_words.append(w)
		elif content_type == 'both':
			self.rm(m=m,w=w,content_type='m')
			self.rm(m=m,w=w,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	def rm_syn(self,m,w,content_type='both'):
		for i in self.get_known_words(m=m):
			if i!=w:
				self.rm(m,i,content_type=content_type)

	def rm_hom(self,m,w,content_type='both'):
		for i in self.get_known_meanings(w=w):
			if i!=m:
				self.rm(i,w,content_type=content_type)

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			return self._content_w.keys()
		else:
			if option is None:
				try:
					return self._content_m[m].keys()
				except KeyError:
					return []
			elif option == 'max':
				val_list = self._content_m[m].items()
				val_max = max([v1 for w1,v1 in val_list])
				return [w1 for w1,v1 in val_list if v1 == val_max]
			elif option == 'min':
				val_list = self._content_m[m].items()
				val_min = min([v1 for w1,v1 in val_list])
				return [w1 for w1,v1 in val_list if v1 == val_min]
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':

	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			return self._content_m.keys()
		else:
			if option is None:
				try:
					return self._content_w[w].keys()
				except KeyError:
					return []
			elif option == 'max':
				val_list = self._content_w[w].items()
				val_max = max([v1 for m1,v1 in val_list])
				return [m1 for m1,v1 in val_list if v1 == val_max]
			elif option == 'min':
				val_list = self._content_w[w].items()
				val_min = min([v1 for m1,v1 in val_list])
				return [m1 for m1,v1 in val_list if v1 == val_min]
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':



	def diagnostic(self):
		print self._cache
		print self

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


	@voc_cache
	def get_accessible_meanings(self):
		return list(self.get_known_meanings())+list(self.unknown_meanings)

	@voc_cache
	def get_accessible_words(self):
		return list(self.get_known_words())+list(self.unknown_words)

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

	def discover_meanings(self,m_list):
		m_list_bis = [m for m in m_list if m not in self.get_known_meanings()+self.unknown_meanings]
		self.unknown_meanings += m_list_bis

	def discover_words(self,w_list):
		w_list_bis = [w for w in w_list if w not in self.get_known_words()+self.unknown_words]
		self.unknown_words += w_list_bis

	def get_unknown_meanings(self):
		return self.unknown_meanings

	def get_unknown_words(self):
		return self.unknown_words

	def get_M(self):
		return self.get_UM()+self.get_KM()

	def get_W(self):
		return self.get_UW()+self.get_KW()

	def get_UM(self):
		return len(self.unknown_meanings)

	def get_UW(self):
		return len(self.unknown_words)

	def get_KM(self):
		return len(self._content_m)

	def get_KW(self):
		return len(self._content_w)

	def get_alterable_shallow_copy(self):
		#return copy.deepcopy(self)
		return AlterableShallowCopyVoc2DictDict(voc=self)

	#def inherit_from: to split a meaning or a word




class AlterableShallowCopyVoc2DictDict(Voc2DictDict):

	def __init__(self,voc,start='empty',**voc_cfg2):
		self.original_voc = voc
		Voc2DictDict.__init__(self,start=start,**voc_cfg2)
		self.rm_list = {'m':[],'w':[]}
		self.unknown_words = self.original_voc.unknown_words[:] #shallow copies of lists
		self.unknown_meanings = self.original_voc.unknown_meanings[:]


	def empty(self):
		raise Exception('Emptying shallow copy not implemented')

	def rm(self,m,w,content_type='both'):
		if content_type == 'm':
			if (m in self.original_voc._content_m.keys() and w in self.original_voc._content_m[m].keys()):
				if (m,w) not in self.rm_list['m']:
					self.rm_list['m'].append((m,w))
			Voc2DictDict.rm(self,m=m,w=w,content_type='m')
		elif content_type == 'w':
			if (w in self.original_voc._content_w.keys() and m in self.original_voc._content_w[w].keys()):
				if (m,w) not in self.rm_list['w']:
					self.rm_list['w'].append((m,w))
			Voc2DictDict.rm(self,m=m,w=w,content_type='w')
		elif content_type == 'both':
			self.rm(m=m,w=w,content_type='m')
			self.rm(m=m,w=w,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	def get_value(self,m,w,content_type='m'):
		if (m,w) in self.rm_list[content_type]:
			return 0.
		else:
			try:
				if content_type == 'm':
					return self._content_m[m][w]
				elif content_type == 'w':
					return self._content_w[w][m]
				else:
					raise ValueError('unknown content type:'+str(content_type))
			except KeyError:
				return self.original_voc.get_value(m,w,content_type)

	def add(self,m,w,val=1,context=[],content_type='both'):
		if val > 0:
			if content_type in ['both','m']:
				if (m,w) in self.rm_list['m']:
					self.rm_list['m'].remove((m,w))
			if content_type in ['both','w']:
				if (m,w) in self.rm_list['w']:
					self.rm_list['w'].remove((m,w))
		Voc2DictDict.add(self,m=m,w=w,val=val,context=context,content_type=content_type)


	def get_KM(self):
		return len(self.get_known_meanings())#could do better by storing explicitly which values are in both self._content_x and self.original_voc._content_x

	def get_KW(self):
		return len(self.get_known_words())#could do better by storing explicitly which values are in both self._content_x and self.original_voc._content_x

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		local = Voc2DictDict.get_known_words(self,m=m,option=option)
		orig = self.original_voc.get_known_words(m=m,option=option)
		return list(set(local) | set(orig))
	

	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		local = Voc2DictDict.get_known_meanings(self,w=w,option=option)
		orig = self.original_voc.get_known_meanings(w=w,option=option)
		return list(set(local) | set(orig))

