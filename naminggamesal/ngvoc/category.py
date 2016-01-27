#!/usr/bin/python

import random
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import sparse
from scipy import misc
import string
from intervaltree import IntervalTree, Interval
import copy
import colorsys

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
		self.minmax_slice(m=m,w=w,context=context)
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
	def slice_intervaltree(self,m1,m2,w1=[],w2=[]):
		if not isinstance(w1,list):
			w1 = [w1]
		if not isinstance(w2,list):
			w2 = [w2]
		if min(m1,m2) == m1:
			m_1 = m1
			w_1 = w1
			m_2 = m2
			w_2 = w2
		else:
			m_1 = m2
			w_1 = w2
			m_2 = m1
			w_2 = w1
		if m_1 < 0 or m_2 > 1:
			return None
		if self.get_category(m1) == self.get_category(m2):
			def datafunc(iv,islower):
				if islower:
					w = [ word for word in w_1 if word not in iv.data ]
					return copy.deepcopy(iv.data) + copy.deepcopy(w)
				else:
					w = [ word for word in w_2 if word not in iv.data ]
					return copy.deepcopy(iv.data) + copy.deepcopy(w)
			self._content_coding.slice((m_1+m_2)/2., datafunc)

	@del_cache
	def minmax_slice(self,m,w=[],context=[],new_words=True):
		ct_maxinf = max([-1] + [m1 for m1 in context if m1 < m])
		ct_minsup = min([2] + [m2 for m2 in context if m2 > m])
		if new_words:
			if not w:
				w = self.get_new_unknown_w()
			w1 = self.get_new_unknown_w()
			w2 = self.get_new_unknown_w()
		else:
			w1 = []
			w2 = []

		self.slice_intervaltree(m,ct_maxinf,w,w1)
		self.slice_intervaltree(m,ct_minsup,w,w2)

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
			for iv in sorted(self._content_coding):
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



	def visual(self, env=None, X=500, Y=20):
		list_perceptual = []
		list_semantic = []
		data = None
		for iv in sorted(self._content_coding):
			list_perceptual.append(iv.begin)
			if data != iv.data:
				list_semantic.append(iv.begin)
				data = iv.data
		list_semantic.append(1.)
		list_perceptual.append(1.)

		im = np.ones((Y,X,3))

		for x in range(X):
			for y in range(Y/2, Y):
				im[y,x,:] = colorsys.hsv_to_rgb((x)/(X-1.),1.,1.)

		for p in list_perceptual:
			x = min(int(p*X),X-1)
			for y in range(Y/4,3*Y/4):
				im[y,x,:] = (0.,0.,0.)

		for p in list_semantic:
			x = min(int(p*X),X-1)
			for y in range(Y):
				im[y,x,:] = (0.,0.,0.)

		plt.figure()
		plt.imshow(im,interpolation='nearest')
		plt.axis('off')
		plt.show()



