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

	def __init__(self, M, W, start='empty',**voc_cfg2):
		self._M = M
		self._W = W
		#self._size = [self._M,self._W]
		#M = voc_cfg2['M']
		#W = voc_cfg2['W']
		BaseVocabulary.__init__(self,**voc_cfg2)
		self._content=np.matrix(np.zeros((self._M,self._W)))
		if start == 'completed':
			self.complete_empty()

	@del_cache
	def complete_empty(self):
		assert len(self.get_known_meanings()) == 0
		print "complete_empty not implemented yet"

	@voc_cache
	def exists(self,m,w):
		if self._content_m[m][w] > 0 or self._content_w[w][m] > 0:
			return 1
		else:
			return 0

	def get_value(self,m,w):
		return self._content_m[m][w]

	def get_content(self,content_type='m'):
		if content_type == 'm':
			return self._content_m
		elif content_type == 'w':
			return self._content_w
		else:
			raise ValueError('unknown content type:'+str(content_type))

	def get_size(self):
		return [self._M,self._W]


	@del_cache
	def add(self,m,w,val=1,context=[],content_type='both'):
		if content_type == 'm':
			if m not in self._content_m.keys():
				self._content_m[m] = {}
			self._content_m[m][w] = val
		elif content_type == 'w':
			if w not in self._content_w.keys():
				self._content_w[w] = {}
			self._content_w[w][m] = val
		elif content_type == 'both':
			self.add(m=m,w=w,val=val,context=context,content_type='m')
			self.add(m=m,w=w,val=val,context=context,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	@del_cache
	def rm(self,m,w,content_type='both'):
		if content_type == 'm':
			del self._content_m[m][w]
			if self._content_m[m] == {}:
				del self._content_m[m]
		elif content_type == 'w':
			del self._content_w[w][m]
			if self._content_w[w] == {}:
				del self._content_w[w]
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

	def get_known_words(self,m=None,option=None):
		if m is None:
			return len(self._content_w)
		else:
			if option is None:
				try:
					return len(self._content_m[m])
				except KeyError:
					return 0
			elif option == 'max':
				val_list = self._content_m[m].items()
				val_max = max([v1 for w1,v1 in val_list])
				return ([w1 for w1,v1 in val_list if v1 == val_max])
			elif option == 'min':
				val_list = self._content_m[m].items()
				val_min = min([v1 for w1,v1 in val_list])
				return ([w1 for w1,v1 in val_list if v1 == val_min])
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':


	def get_known_meanings(self,w=None,option=None):
		if w is None:
			return len(self._content_m)
		else:
			if option is None:
				try:
					return len(self._content_w[w])
				except KeyError:
					return 0
			elif option == 'max':
				val_list = self._content_w[w].items()
				val_max = max([v1 for m1,v1 in val_list])
				return ([m1 for m1,v1 in val_list if v1 == val_max])
			elif option == 'min':
				val_list = self._content_w[w].items()
				val_min = min([v1 for m1,v1 in val_list])
				return ([m1 for m1,v1 in val_list if v1 == val_min])
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






	def get_random_m(self):
		return random.choice(range(self._M)) #random from known+explored+adjacent_possible

	def get_new_unknown_m(self):
		if not len(self.get_known_meanings()) == self._M:
			m = random.choice(self.get_unknown_meanings())
		else:
			#print "tried to get new m but all are known"
			m = self.get_random_known_m()
		return m

	def get_new_unknown_w(self):
		if hasattr(self,'next_word'):
			w = self.next_word
			delattr(self,'next_word')
		elif not len(self.get_known_words()) == self._W:
			w = random.choice(self.get_unknown_words())
		else:
			#print "tried to get new w but all are known"
			w = self.get_random_known_w()
		return w



	#def inherit_from: to split a meaning or a word