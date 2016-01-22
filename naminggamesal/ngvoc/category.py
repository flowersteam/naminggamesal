#!/usr/bin/python

import random
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import sparse
import string
from intervaltree import IntervalTree, Interval
import copy

from . import BaseVocabulary
from . import voc_cache, del_cache


VOWELS = "aeiou"
CONSONANTS = "".join(set(string.lowercase) - set(VOWELS))

class VocCategory(BaseVocabulary):

	def __init__(self, shape=1, **voc_cfg2):
		BaseVocabulary.__init__(self,**voc_cfg2)
		self._content_coding = IntervalTree([Interval(0,1,[])])
		self._content_decoding = {}

	@voc_cache
	def get_category(self, m):
		return sorted(self._content_coding[m])[0]

	@voc_cache
	def exists(self,m,w):
		if w in self.get_category(m).data:
			return True
		else:
			return False

	def get_content(self):
		return copy.deepcopy([self._content_coding, self._content_decoding])

	def get_size(self):
		return [self.get_M(),self.get_W()]

	@voc_cache
	def get_W(self):
		return self._content_decoding.keys()

	@voc_cache
	def get_M(self):
		data = None
		iv_l = sorted(self._content_coding)
		for i in iv_l:
			if i.data != data:
				M += 1
				data = i.data
		return M

	@del_cache
	def add(self,m,w,context=[]):
		self.minmax_slice(m,context,new_words=False)
		if w not in self.get_category(m).data:
			self.get_category(m).data.append(w)
		if self.get_category(m) not in self._content_decoding.setdefault(w,IntervalTree()):
			self._content_decoding[w].add(self.get_category(m))
			self._content_decoding[w].merge_overlaps()

	def datafunc_slicing(self,iv,islower):
		return copy.deepcopy(iv.data) + [self.get_new_unknown_w()]

	def datafunc_chopping(self,iv,islower):
		return copy.deepcopy(iv.data)

	@del_cache
	def slice_intervaltree(self,m1,m2,new_words=True):
		if m1 < 0 or m2 < 0 or m1 > 1 or m2 > 1:
			return None
		if self.get_category(m1) == self.get_category(m2):
			if new_words:
				self._content_coding.slice((m1+m2)/2., self.datafunc_slicing)
			else:
				self._content_coding.slice((m1+m2)/2., self.datafunc_chopping)

	@del_cache
	def minmax_slice(self,m,context,new_words=True):
		ct_maxinf = max([-1] + [m1 for m1 in context if m1 < m])
		ct_minsup = min([2] + [m2 for m2 in context if m2 > m])
		self.slice_intervaltree(m,ct_maxinf,new_words=new_words)
		self.slice_intervaltree(m,ct_minsup,new_words=new_words)

	@del_cache
	def rm(self,m,w):
		if w in self.get_category(m).data:
			self.get_category(m).data.remove(w)
		if w in self._content_decoding.keys() and self._content_decoding[w][m]:
			self._content_decoding[w].chop(self.get_category(m).begin,self.get_category(m).end,self.datafunc_chopping)
			if not self._content_decoding[w]:
				del self._content_decoding[w]



	def get_random_m(self):
		return random.random()



	def rm_syn(self,m,w):
		to_rm = []
		for i in self.get_known_words(m=m):
			if i!=w:
				to_rm.append(i)
		for i in to_rm:
			self.rm(m,i)

	def rm_hom(self,m,w):
		to_rm = []
		for iv in self.get_known_meanings(w=w):
			for iv2 in self._content_coding[iv.begin:iv.end]:
				if not iv2.contains_point(m):
					to_rm.append(iv2)
		for iv2 in to_rm:
			self.rm((iv2.begin+iv2.end)/2.,w)



	@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			return self._content_decoding.keys()
		else:
			return self.get_category(m).data

	@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			new_tree = IntervalTree()
			data = None
			begin = 0
			for iv in self._content_coding:
				if iv.data != data:
					if data:
						new_tree.add(Interval(begin, iv.end))
					begin = iv.end
					data = iv.data
			return new_tree
		elif w in self._content_decoding.keys():
			return self._content_decoding[w]
		else:
			return []

	@voc_cache
	def get_unknown_meanings(self, w=None,option=None):
		ivt = IntervalTree([Interval(iv.begin,iv.end) for iv in self._content_coding if not iv.data])
		ivt.merge_overlaps()
		return ivt

	def get_new_unknown_m(self):
		return self.get_random_element(self.get_unknown_meanings())

	def get_random_element(self, ivt):
		seq = []
		p = []
		total_length = 0
		for iv in ivt:
			seq.append(iv)
			p.append(len(iv))
			total_length += len(iv)
		p_norm = [p_el / float(total_length) for p_el in p]
		iv = seq[np.random.choice(len(seq),p=p_norm)]
		return random.random()*len(iv) + iv.begin

	def get_new_unknown_w(self):
		w = ''
		for i in range(3):
			w += random.choice(CONSONANTS)
			w += random.choice(VOWELS)
		return w

	def get_random_known_m(self,w=None,option=None):
		if w is None:
			if not self.get_known_meanings():
				return self.get_random_m()
			else:
				return self.get_random_element(self.get_known_meanings())
		else:
			if not w in self._content_decoding.keys() or not self._content_decoding[w]:
				return self.get_random_m()
			else:
				return self.get_random_element(self._content_decoding[w])

	def get_random_known_w(self,m=None,option=None):
		if m is None:
			if not self._content_decoding.keys():
				return self.get_new_unknown_w()
			else:
				return random.choice(self._content_decoding.keys())
		else:
			if not self.get_category(m).data:
				return self.get_new_unknown_w()
			else:
				return random.choice(self.get_category(m).data)
