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
		#return len(self._content_m)
		return len(self.get_accessible_meanings())-len(self.unknown_meanings)

	def get_KW(self):
		#return len(self._content_w)
		return len(self.get_accessible_words())-len(self.unknown_words)

	def get_alterable_shallow_copy(self):
		return copy.deepcopy(self)
		#return AlterableShallowCopyVoc2DictDict(voc=self)

	#def inherit_from: to split a meaning or a word

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is not None:
			m_idx = self.meaning_indexes[m]
		if m is None:
			return list(set(self.get_accessible_words())-set(self.unknown_words))
		elif option is None:
			selection = self._content_m[m_idx,:]
			ans = self.get_coords(option=option,mat=selection,m_idx=m_idx)
			#ans = list(set(list(selection.nonzero()[0])))
			return [self.indexes_word[www[1]] for www in ans]
		elif option == 'max':
			selection = self._content_m[m_idx,:]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection,m_idx=m_idx)
			#ans = list(set(list(np.argwhere(selection == np.amax(selection[nz])).reshape((-1)))))
			return [self.indexes_word[www[1]] for www in ans]
		elif option == 'min':
			selection = self._content_m[m_idx,:]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection,m_idx=m_idx)
			#ans = list(set(list(np.argwhere(selection == np.amin(selection[nz])).reshape((-1)))))
			return [self.indexes_word[www[1]] for www in ans]


	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is not None:
			w_idx = self.word_indexes[w]
		if w is None:
			return list(set(self.get_accessible_meanings())-set(self.unknown_meanings))
		elif option is None:
			selection = self._content_w[:,w_idx]
			ans = self.get_coords(option=option,mat=selection,w_idx=w_idx)
			#ans = list(set(list(selection.nonzero()[0])))
			return [self.indexes_meaning[mmm[0]] for mmm in ans]
		elif option == 'max':
			selection = self._content_w[:,w_idx]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection,w_idx=w_idx)
			#ans = list(set(list(np.argwhere(selection == np.amax(selection[nz])).reshape((-1)))))
			return [self.indexes_meaning[mmm[0]] for mmm in ans]
		elif option == 'min':
			selection = self._content_w[:,w_idx]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection,w_idx=w_idx)
			#ans = list(set(list(np.argwhere(selection == np.amin(selection[nz])).reshape((-1)))))
			return [self.indexes_meaning[mmm[0]] for mmm in ans]

	#@voc_cache
	def get_known_meanings_weights(self,w):
		pass

	#@voc_cache
	def get_known_words_weights(self,m):
		pass


	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		w_idx = self.word_indexes[w]
		selection = self._content_w[:,w_idx]
		nz = selection.nonzero()
		ans = list(selection[nz])
		#return selection.reshape((1, len(self.get_accessible_meanings())))
		return selection.tolist()

	#@voc_cache
	def get_known_words_weights_values(self,m):
		m_idx = self.meaning_indexes[m]
		selection = self._content_m[m_idx,:]
		nz = selection.nonzero()
		ans = list(selection[nz])
		#return selection.reshape((1, len(self.get_accessible_words())))
		return selection.tolist()

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
			gkw = self.get_known_words(m=m)
			if len(gkw) == 1 and w in gkw:
				self.unknown_meanings.append(m)
			self._content_m[m_idx,w_idx] = 0
		elif content_type == 'w':
			m_idx = self.meaning_indexes[m]
			w_idx = self.word_indexes[w]
			gkm = self.get_known_meanings(w=w)
			if len(gkm) == 1 and m in gkm:
				self.unknown_words.append(w)
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

	def discover_meanings(self,m_list,weights=None):
		m_list_bis = BaseVocabularyElaborated.discover_meanings(self,m_list=m_list,weights=weights)
		if not hasattr(self,'meaning_indexes'):
			self.meaning_indexes = {}
			self.indexes_meaning = {}
		max_ind = len(list(self.meaning_indexes.keys()))-1
		for mm in m_list_bis:
			max_ind += 1
			self.meaning_indexes[mm] = max_ind
			self.indexes_meaning[max_ind] = mm
		self.update_vocshape()
		return m_list_bis


	def discover_words(self,w_list,weights=None):
		w_list_bis = BaseVocabularyElaborated.discover_words(self,w_list=w_list,weights=weights)
		if not hasattr(self,'word_indexes'):
			self.word_indexes = {}
			self.indexes_word = {}
		max_ind = len(list(self.word_indexes.keys()))-1
		for ww in w_list_bis:
			max_ind += 1
			self.word_indexes[ww] = max_ind
			self.indexes_word[max_ind] = ww
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
			#new_w[:(M1-M),:(W1-W)] = self._content_w
			new_w[:M1,:W1] = self._content_w
		if M2*W2 != 0:
			new_w[:M2,:W2] = self._content_m
		self._content_w = new_w
		self._content_m = new_m

	def get_coords(self,mat,option=None,w_idx=None,m_idx=None):
		nz = mat.nonzero()
		if not nz[0].size:
			return []
		if option is None:
			return self.get_coords_none(mat,nz=nz,w_idx=w_idx,m_idx=m_idx)
		elif option == 'max':
			return self.get_coords_max(mat,nz=nz,w_idx=w_idx,m_idx=m_idx)
		elif option == 'min':
			return self.get_coords_min(mat,nz=nz,w_idx=w_idx,m_idx=m_idx)
		elif option == 'minofmaxw':
			return self.get_coords_minofmaxw(mat,nz=nz,w_idx=w_idx,m_idx=m_idx)
		elif option == 'minofmaxm':
			return self.get_coords_minofmaxm(mat,nz=nz,w_idx=w_idx,m_idx=m_idx)

	def get_coords_none(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		return self.add_coord(nz[0],w_idx=w_idx,m_idx=m_idx)

	def add_coord(self,coords,m_idx=None,w_idx=None):
		if w_idx is not None:
			coords_output = [(nn,w_idx) for nn in coords]
		elif m_idx is not None:
			coords_output = [(m_idx,nn) for nn in coords]
		else:
			coords_output = coords
		return coords_output

	def get_coords_max(self,mat,nz=None,m_idx=None,w_idx=None):
		if nz is None:
			nz = mat.nonzero()
		coords = np.argwhere(mat == np.amax(mat[nz]))
		#coords = coords.reshape((-1,2))
		return self.add_coord(coords.reshape((-1)).tolist(),w_idx=w_idx,m_idx=m_idx)

	def get_coords_min(self,mat,nz=None,m_idx=None,w_idx=None):
		if nz is None:
			nz = mat.nonzero()
		coords = np.argwhere(mat == np.amin(mat[nz]))
		#coords = coords.reshape((-1,2))
		return self.add_coord(coords.reshape((-1)).tolist(),w_idx=w_idx,m_idx=m_idx)

	def get_coords_minofmaxw(self,mat,nz=None,m_idx=None,w_idx=None):
		best_scores = mat.max(axis=0)
		val = np.amin(best_scores)
		coords = np.argwhere(best_scores == val)
		#coords = coords.reshape((-1,2))
		return self.add_coord(coords.reshape((-1)).tolist(),w_idx=w_idx,m_idx=m_idx)

	def get_coords_minofmaxm(self,mat,nz=None,m_idx=None,w_idx=None):
		best_scores = mat.max(axis=1)
		val = np.amin(best_scores)
		coords = np.argwhere(best_scores == val)
		#coords = coords.reshape((-1,2))
		return self.add_coord(coords.reshape((-1)).tolist(),w_idx=w_idx,m_idx=m_idx)

	@classmethod
	def srtheo_voc(cls,voc1,voc2=None,m=None,w=None,role='both'):
		if role == 'speaker':
			m1 = copy.deepcopy(voc1._content_m)
			m2 = copy.deepcopy(voc2._content_w)
			if not hasattr(voc1,'is_normalized') or not voc1.is_normalized:
				m1 = cls.norm(mat=m1,axis=1)
			if not hasattr(voc2,'is_normalized') or not voc2.is_normalized:
				m2 = cls.norm(mat=m2,axis=0)
			try:
				prefactor = 1./voc1.get_M()
			except ZeroDivisionError:
				return 0
			if m is not None and w is not None:
				m_idx = voc1.meaning_indexes[m]
				m_idx2 = voc2.meaning_indexes[m]
				w_idx = voc1.word_indexes[w]
				w_idx2 = voc2.word_indexes[w]
				return m1[m_idx,w_idx]*m2[m_idx2,w_idx2]
			elif m is not None:
				m_idx = voc1.meaning_indexes[m]
				assert m_idx == voc2.meaning_indexes[m]
				m1 = m1[m_idx,:]
				m2 = m2[m_idx,:]
				tempval = cls.mult_sum(m1,m2)
				return tempval
			elif w is not None:
				raise NotImplementedError
				#w_idx = voc1.word_indexes[w]
				#assert w_idx == voc2.word_indexes[w]
				#m1 = m1[:,w_idx]
				#m2 = m2[:,w_idx]
				#prefactor2 = cls.count_nonzero(m1)
				#tempval = cls.mult_sum(m1,m2)
				#return tempval * prefactor2
			else:
				tempval = cls.mult_sum(m1,m2)
				return prefactor * tempval
		elif role == 'hearer':
			return cls.srtheo_voc(voc1=voc2,voc2=voc1,m=m,w=w,role='speaker')
		elif role == 'both':
			return 0.5*(cls.srtheo_voc(voc1=voc1,voc2=voc2,m=m,w=w,role='speaker')+cls.srtheo_voc(voc1=voc1,voc2=voc2,m=m,w=w,role='hearer'))

	@classmethod
	def norm(cls,mat,axis=0):
		with np.errstate(divide='ignore'):
			divmat = np.nan_to_num(1/ np.linalg.norm(mat, axis=axis, ord=1,keepdims=True))
		return mat *divmat

	@classmethod
	def mult_sum(cls,m1,m2):
		mult = np.multiply(m1,m2)
		return np.nan_to_num(mult).sum()

	@classmethod
	def count_nonzero(cls,m1):
		return np.count_nonzero(m1)

class VocSparseNew(VocMatrixNew):

	def init_empty_content(self,option='m'):
		if option == 'm':
			return sparse.csr_matrix((len(self.get_accessible_meanings()),len(self.get_accessible_words())))
		elif option == 'w':
			return sparse.csc_matrix((len(self.get_accessible_meanings()),len(self.get_accessible_words())))
		else:
			raise ValueError('no such option: '+str(option))


	@del_cache
	def rm(self,m,w,content_type='both'):
		VocMatrixNew.rm(self,m=m,w=w,content_type=content_type)
		self._content_m.eliminate_zeros()
		self._content_w.eliminate_zeros()

	def get_coords_none(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i],nz[1][i]) for i in range(len(nz[0]))] #tolist??
		return self.add_coord(coords,w_idx=w_idx,m_idx=m_idx)

	def get_coords_max(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i[0]],nz[1][i[0]]) for i in np.argwhere(mat.data == mat.data.max()) if mat.data.any()]
		return self.add_coord(coords,w_idx=w_idx,m_idx=m_idx)

	def get_coords_min(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i[0]],nz[1][i[0]]) for i in np.argwhere(mat.data == mat.data.min()) if mat.data.any()]
		return self.add_coord(coords,w_idx=w_idx,m_idx=m_idx)

	def get_coords_minofmaxm(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		meanings = self.get_known_meanings(option=None)
		best_scores = np.zeros(len(meanings))
		for i in range(len(nz[0])):
			m = nz[0][i]
			w = nz[1][i]
			index_m = np.argwhere(meanings == m).reshape((-1))[0]
			best_scores[index_m] = max(best_scores[index_m],mat[m,w])
		val = np.amin(best_scores)
		coords_m = np.argwhere(best_scores == val).reshape((-1))
		coords = []
		for m_i in coords_m:
			coords += [(m_i,w_i) for w_i in self.get_known_words(m=m_i,option='max')]
		return self.add_coord(coords,w_idx=w_idx,m_idx=m_idx)

	def get_coords_minofmaxw(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		words = self.get_known_words(option=None)
		best_scores = np.zeros(len(words))
		for i in range(len(nz[0])):
			m = nz[0][i]
			w = nz[1][i]
			index_w = np.argwhere(words == w).reshape((-1))[0]
			best_scores[index_w] = max(best_scores[index_w],mat[m,w])
		val = np.amin(best_scores)
		coords_w = np.argwhere(best_scores == val).reshape((-1))
		coords = []
		for w_i in coords_w:
			coords += [(m_i,w_i) for m_i in self.get_known_meanings(w=w_i,option='max')]
		return self.add_coord(coords,w_idx=w_idx,m_idx=m_idx)

	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		w_idx = self.word_indexes[w]
		return self._content_w.getcol(w_idx).todense().reshape(-1).tolist()[0]

	#@voc_cache
	def get_known_words_weights_values(self,m):
		m_idx = self.meaning_indexes[m]
		return self._content_m.getrow(m_idx).todense().tolist()[0]

	@classmethod
	def norm(cls,mat,axis=0):
		with np.errstate(divide='ignore'):
			normvec = scipy.sparse.linalg.norm(mat, axis=axis, ord=1)
			normvec = np.matrix(normvec)
			if axis == 1:
				normvec = normvec.transpose()
			divmat = np.nan_to_num(1/ normvec)#,keepdims=True))
			if mat.__class__ == sparse.csr.csr_matrix:
				return mat.multiply(divmat).tocsr()
			elif mat.__class__ == sparse.csc.csc_matrix:
				return mat.multiply(divmat).tocsc()
			else:
				return mat.multiply(divmat)


	@classmethod
	def mult_sum(cls,m1,m2):
		mult = m1.multiply(m2)
		return mult.sum()

	@classmethod
	def count_nonzero(cls,m1):
		return m1.getnnz()

	def add_coord(self,coords,m_idx=None,w_idx=None):
		return coords