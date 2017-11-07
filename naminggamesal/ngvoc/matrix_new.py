#!/usr/bin/python

import random
import numpy as np
import copy
import scipy
from scipy import sparse

from . import BaseVocabulary,BaseVocabularyElaborated
from . import voc_cache, del_cache


class VocMatrixNew(BaseVocabularyElaborated):

	def init_empty_content(self,option='m'):
		return np.zeros((len(self.get_accessible_meanings()),len(self.get_accessible_words())))

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
		if m is None:
			return list(set(self.get_accessible_words())-set(self.unknown_words))
		elif option is None:
			selection = self._content_m[m,:]
			ans = list(selection.nonzero()[0])
			return ans
		elif option == 'max':
			selection = self._content_m[m,:]
			nz = selection.nonzero()
			ans = list(np.argwhere(selection == np.amax(selection[nz])).reshape((-1)))
			return ans
		elif option == 'min':
			selection = self._content_m[m,:]
			nz = selection.nonzero()
			ans = list(np.argwhere(selection == np.amin(selection[nz])).reshape((-1)))
			return ans


	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			return list(set(self.get_accessible_meanings())-set(self.unknown_meanings))
		elif option is None:
			selection = self._content_w[w,:]
			ans = list(selection.nonzero()[0])
			return ans
		elif option == 'max':
			selection = self._content_w[w,:]
			nz = selection.nonzero()
			ans = list(np.argwhere(selection == np.amax(selection[nz])).reshape((-1)))
			return ans
		elif option == 'min':
			selection = self._content_w[w,:]
			nz = selection.nonzero()
			ans = list(np.argwhere(selection == np.amin(selection[nz])).reshape((-1)))
			return ans

	#@voc_cache
	def get_known_meanings_weights(self,w):
		pass

	#@voc_cache
	def get_known_words_weights(self,m):
		pass

	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		selection = self._content_w[w,:]
		nz = selection.nonzero()
		ans = list(selection[nz])
		return ans

	#@voc_cache
	def get_known_words_weights_values(self,m):
		selection = self._content_m[m,:]
		nz = selection.nonzero()
		ans = list(selection[nz])
		return ans

	#@voc_cache
	def get_known_meanings_weights_indexes(self,w):
		pass

	#@voc_cache
	def get_known_words_weights_indexes(self,m):
		pass

	@del_cache
	def add(self,m,w,val=1,context=[],content_type='both'):
		assert m in self.get_accessible_meanings()
		assert w in self.get_accessible_words()
		#if hasattr(self,'valmax') and val > self.valmax:
		#	val = self.valmax
		if val <= 0:
			self.rm(m,w,content_type=content_type)
		else:
			if content_type == 'm':
				m_idx = self.meaning_indexes[m]
				w_idx = self.word_indexes[w]
				self._content_m[m_idx,w_idx] = val
				if m in self.unknown_meanings:
					self.unknown_meanings.remove(m)
				#if w in self.unknown_words:
				#	self.unknown_words.remove(w)
			elif content_type == 'w':
				m_idx = self.meaning_indexes[m]
				w_idx = self.word_indexes[w]
				self._content_w[m_idx,w_idx] = val
				#if m in self.unknown_meanings:
				#	self.unknown_meanings.remove(m)
				if w in self.unknown_words:
					self.unknown_words.remove(w)
			elif content_type == 'both':
				self.add(m=m,w=w,val=val,context=context,content_type='m')
				self.add(m=m,w=w,val=val,context=context,content_type='w')
			else:
				raise ValueError('unknown content type:'+str(content_type))

	@del_cache
	def rm(self,m,w,content_type='both'):
		assert m in self.get_accessible_meanings()
		assert w in self.get_accessible_words()
		if content_type == 'm':
			m_idx = self.meaning_indexes[m]
			w_idx = self.word_indexes[w]
			self._content_m[m_idx,w_idx] = 0
		elif content_type == 'w':
			m_idx = self.meaning_indexes[m]
			w_idx = self.word_indexes[w]
			self._content_w[m_idx,w_idx] = 0
		elif content_type == 'both':
			self.rm(m=m,w=w,content_type='m')
			self.rm(m=m,w=w,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	def get_value(self,m,w,content_type='m'):
		m_idx = self.meaning_indexes[m]
		w_idx = self.word_indexes[w]
		if content_type == 'm':
			return self._content_m[m_idx,w_idx]
		if content_type == 'w':
			return self._content_w[m_idx,w_idx]
		else:
			raise ValueError('content type nopt recognized')

	def rm_syn(self,m,w,content_type='both'):
		for i in self.get_known_words(m=m):
			if i!=w:
				self.rm(m,i,content_type=content_type)

	def rm_hom(self,m,w,content_type='both'):
		for i in self.get_known_meanings(w=w):
			if i!=m:
				self.rm(i,w,content_type=content_type)

	def discover_meanings(self,m_list):
		m_list_bis = BaseVocabularyElaborated.discover_meanings(self,m_list=m_list)
		if not hasattr(self,'meaning_indexes'):
			self.meaning_indexes = {}
		max_ind = len(list(self.meaning_indexes.keys()))-1
		for mm in m_list_bis:
			max_ind += 1
			self.meaning_indexes[mm] = max_ind
		self.update_vocshape()
		return m_list_bis



	def discover_words(self,w_list):
		w_list_bis = BaseVocabularyElaborated.discover_words(self,w_list=w_list)
		if not hasattr(self,'word_indexes'):
			self.word_indexes = {}
		max_ind = len(list(self.word_indexes.keys()))-1
		for ww in w_list_bis:
			max_ind += 1
			self.word_indexes[ww] = max_ind
		self.update_vocshape()
		return w_list_bis

	def update_vocshape(self):
		M = len(self.get_accessible_meanings())
		W = len(self.get_accessible_words())
		new_w = self.init_empty_content()
		new_m = self.init_empty_content()
		M1,W1 = self._content_w.shape
		M2,W2 = self._content_m.shape
		if M1*W1 != 0:
			new_w[:(M-M1),:(W-W1)] = self._content_w
		if M2*W2 != 0:
			new_w[:(M-M2),:(W-W2)] = self._content_m
		self._content_w = new_w
		self._content_m = new_m