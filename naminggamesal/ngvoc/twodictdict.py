#!/usr/bin/python

import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import scipy
from scipy import sparse

from . import BaseVocabulary,BaseVocabularyElaborated
from . import voc_cache, del_cache




class Voc2DictDict(BaseVocabularyElaborated):


	def init_empty_content(self,option='m'):
		return {}

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
				if m not in list(self._content_m.keys()):#self.get_known_meanings():
					self._content_m[m] = {}
				self._content_m[m][w] = val
				if m in self.unknown_meanings:
					self.unknown_meanings.remove(m)
				#if w in self.unknown_words:
				#	self.unknown_words.remove(w)
			elif content_type == 'w':
				if w not in list(self._content_w.keys()):#self.get_known_words():
					self._content_w[w] = {}
				self._content_w[w][m] = val
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
			if m in list(self._content_m.keys()) and w in list(self._content_m[m].keys()):
				del self._content_m[m][w]
				if self._content_m[m] == {}:
					del self._content_m[m]
					self.unknown_meanings.append(m)
		elif content_type == 'w':
			if w in list(self._content_w.keys()) and m in list(self._content_w[w].keys()):
				del self._content_w[w][m]
				if self._content_w[w] == {}:
					del self._content_w[w]
					self.unknown_words.append(w)
		elif content_type == 'both':
			self.rm(m=m,w=w,content_type='m')
			self.rm(m=m,w=w,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			return list(self._content_w.keys())
		else:
			if option is None:
				try:
					return list(self._content_m[m].keys())
				except KeyError:
					return []
			elif option == 'max':
				val_list = list(self._content_m[m].values())
				item_list = list(self._content_m[m].items())
				val_max = max(val_list)
				return sorted([w1 for w1,v1 in item_list if v1 == val_max])
			elif option == 'min':
				val_list = list(self._content_m[m].values())
				item_list = list(self._content_m[m].items())
				val_min = min(val_list)
				return sorted([w1 for w1,v1 in item_list if v1 == val_min])
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':

	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			return list(self._content_m.keys())
		else:
			if option is None:
				try:
					return list(self._content_w[w].keys())
				except KeyError:
					return []
			elif option == 'max':
				val_list = list(self._content_w[w].values())
				item_list = list(self._content_w[w].items())
				val_max = max(val_list)
				return sorted([m1 for m1,v1 in item_list if v1 == val_max])
			elif option == 'min':
				val_list = list(self._content_w[w].values())
				item_list = list(self._content_w[w].items())
				val_min = min(val_list)
				return sorted([m1 for m1,v1 in item_list if v1 == val_min])
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':


	#@voc_cache
	def get_known_meanings_weights(self,w):
		try:
			return list(self._content_w[w].items())
		except KeyError:
			return []


	#@voc_cache
	def get_known_words_weights(self,m):
		try:
			return list(self._content_m[m].items())
		except KeyError:
			return []

	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		try:
			return list(self._content_w[w].values())
		except KeyError:
			return []

	#@voc_cache
	def get_known_words_weights_values(self,m):
		try:
			return list(self._content_m[m].values())
		except KeyError:
			return []

	def get_alterable_shallow_copy(self):
		return copy.deepcopy(self)
		#return AlterableShallowCopyVoc2DictDict(voc=self)

	#def inherit_from: to split a meaning or a word




class AlterableShallowCopyVoc2DictDict(Voc2DictDict):

	def __init__(self,voc,start='empty',**voc_cfg2):
		self.original_voc = voc
		Voc2DictDict.__init__(self,start=start,**voc_cfg2)
		self.rm_list = {'m':[],'w':[]}
		self.unknown_words = self.original_voc.unknown_words[:] #shallow copies of lists
		self.unknown_meanings = self.original_voc.unknown_meanings[:]


	def empty(self):
		#change original_voc to an empty one, and empty as well features of self?
		raise Exception('Emptying shallow copy not implemented')

	def rm(self,m,w,content_type='both'):
		if content_type == 'm':
			if (m in list(self.original_voc._content_m.keys()) and w in list(self.original_voc._content_m[m].keys())):
				if (m,w) not in self.rm_list['m']:
					self.rm_list['m'].append((m,w))
			Voc2DictDict.rm(self,m=m,w=w,content_type='m')
		elif content_type == 'w':
			if (w in list(self.original_voc._content_w.keys()) and m in list(self.original_voc._content_w[w].keys())):
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
		#return list(set(local) | set(orig))
		return list(set(local + orig))


	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		local = Voc2DictDict.get_known_meanings(self,w=w,option=option)
		orig = self.original_voc.get_known_meanings(w=w,option=option)
		#return list(set(local) | set(orig))
		return list(set(local + orig))

