#!/usr/bin/python

import sys
#if sys.version_info.major < 3:
#	print("WARNING: pandas multiindex do not work properly under python2, you should use another type of vocabulary")

import pandas as pd
from pandas.core.indexing import IndexingError

import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import scipy
from scipy import sparse

from . import BaseVocabulary,BaseVocabularyElaborated
#from .twodictdict import Voc2DictDict
from . import voc_cache, del_cache

import warnings
warnings.warn('pandas based vocabularies should not be used, because of bugs in the pandas lib, especially with MultiIndex and slicing')


def check_1D(var,idx=1):
	try:
		if var:
			a = [v[idx] for v in var]
			return a
		else:
			if var != []:
				return var
			else:
				raise ValueError
	except:
		return var


class VocPandas(BaseVocabularyElaborated):



	def init_empty_content_df(self,option='m'):
		ans = pd.DataFrame(columns=['Meaning','Word','Value'])
		ans.set_index(['Meaning','Word'], inplace=True)
		return ans

	def init_empty_content(self,option='m'):
		idx = pd.MultiIndex(levels=[[],[]],labels=[[],[]],names=[u'Meaning', u'Word'])
		ans = pd.Series(index=idx)
		return ans
#add: df = df.append({'Meaning':m,'Word':w,'Value':v},ignore_index=True)
#note: possibility of multiple add operations at once {'Meaning':[m1,m2],'Word':[w1,w2],'Value':[v1,v2]}
#rm: df = df[df.condition]
#change val : df['foo'] = df['foo'].where(df['foo'] < 0.5, 100)
# changes on the original df: , inplace=True)

	def get_value(self,m,w,content_type='m'):
		try:
			if content_type == 'm':
				#return self._content_m.query('Meaning=='+str(m)+' and Word=='+str(w))['Value'][0]
				tempvoc = copy.deepcopy(self._content_m)
				return tempvoc.loc[m,w]#['Value']#PANDASREPLACENEEDED
			elif content_type == 'w':
				#return self._content_w.query('Meaning=='+str(m)+' and Word=='+str(w))['Value'][0]
				tempvoc = copy.deepcopy(self._content_w)
				return tempvoc.loc[m,w]#['Value']#PANDASREPLACENEEDED
			else:
				raise ValueError('unknown content type:'+str(content_type))
		except KeyError:
			return 0
		except IndexingError:
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
				self._content_m.loc[m,w] = val#PANDASREPLACENEEDED
				if m in self.unknown_meanings:
					self.unknown_meanings.remove(m)
				#if w in self.unknown_words:
				#	self.unknown_words.remove(w)
			elif content_type == 'w':
				self._content_w.loc[m,w] = val#PANDASREPLACENEEDED
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
			try:
				self._content_m.drop((m,w),inplace=True)
				if m not in self.get_known_meanings() and m not in self.unknown_meanings:
					self.unknown_meanings.append(m)
			except KeyError:
				pass
		elif content_type == 'w':
			try:
				self._content_w.drop((m,w),inplace=True)
				if w not in self.get_known_words() and w not in self.unknown_words:
					self.unknown_words.append(w)
			except KeyError:
				pass
		elif content_type == 'both':
			self.rm(m=m,w=w,content_type='m')
			self.rm(m=m,w=w,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			ans = list(self._content_w.index.get_level_values('Word'))#PANDASREPLACENEEDED
			return check_1D(ans,idx=0)
		else:
			if option is None:
				try:
					return self.get_known_words_weights_indexes(m=m)#PANDASREPLACENEEDED
				except KeyError:
					return []
				except IndexingError:
					return []
			elif option == 'max':
				val_list = list(self.get_known_words_weights_values(m))#PANDASREPLACENEEDED
				idx_list = list(self.get_known_words_weights_indexes(m))#PANDASREPLACENEEDED
				item_list = list(zip(idx_list,val_list))
				val_max = max(val_list)
				return sorted([w1 for w1,v1 in item_list if v1 == val_max])
			elif option == 'min':
				val_list = list(self.get_known_words_weights_values(m))#PANDASREPLACENEEDED
				idx_list = list(self.get_known_words_weights_indexes(m))#PANDASREPLACENEEDED
				item_list = list(zip(idx_list,val_list))
				val_min = min(val_list)
				return sorted([w1 for w1,v1 in item_list if v1 == val_min])
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':

	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			return list(self._content_m.index.get_level_values('Meaning'))#PANDASREPLACENEEDED
		else:
			if option is None:
				try:
					return self.get_known_meanings_weights_indexes(w=w)#PANDASREPLACENEEDED
				except KeyError:
					return []
				except IndexingError:
					return []
			elif option == 'max':
				val_list = list(self.get_known_meanings_weights_values(w))#PANDASREPLACENEEDED
				idx_list = list(self.get_known_meanings_weights_indexes(w))#PANDASREPLACENEEDED
				item_list = list(zip(idx_list,val_list))
				val_max = max(val_list)
				return sorted([m1 for m1,v1 in item_list if v1 == val_max])
			elif option == 'min':
				val_list = list(self.get_known_meanings_weights_values(w))#PANDASREPLACENEEDED
				idx_list = list(self.get_known_meanings_weights_indexes(w))#PANDASREPLACENEEDED
				item_list = list(zip(idx_list,val_list))
				val_min = min(val_list)
				return sorted([m1 for m1,v1 in item_list if v1 == val_min])
			#elif option == 'minofmaxw':
			#elif option == 'minofmaxm':


	#@voc_cache
	def get_known_meanings_weights(self,w):
		tempvoc = copy.deepcopy(self._content_w)
		return tempvoc.loc[:,w]#PANDASREPLACENEEDED

	#@voc_cache
	def get_known_words_weights(self,m):
		tempvoc = copy.deepcopy(self._content_m)
		return tempvoc.loc[m,:]#PANDASREPLACENEEDED

	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		ans = list(self.get_known_meanings_weights(w))#PANDASREPLACENEEDED
		return check_1D(ans,idx=1)

	#@voc_cache
	def get_known_words_weights_values(self,m):
		ans = list(self.get_known_words_weights(m))#PANDASREPLACENEEDED
		return check_1D(ans,idx=1)

	#@voc_cache
	def get_known_meanings_weights_indexes(self,w):
		ans = list(self.get_known_meanings_weights(w).index.get_level_values('Meaning'))#PANDASREPLACENEEDED
		return check_1D(ans,idx=0)

	#@voc_cache
	def get_known_words_weights_indexes(self,m):
		ans = list(self.get_known_words_weights(m).index.get_level_values('Word'))#PANDASREPLACENEEDED
		return check_1D(ans,idx=0)

	def get_KM(self):
		return len(self._content_m.index.get_level_values('Meaning'))#PANDASREPLACENEEDED

	def get_KW(self):
		return len(self._content_w.index.get_level_values('Word'))#PANDASREPLACENEEDED

	def get_alterable_shallow_copy(self):
		return copy.deepcopy(self)
		#return AlterableShallowCopyVoc2DictDict(voc=self) 
		# df2 = df.copy() #,deep=True)

	#def inherit_from: to split a meaning or a word
