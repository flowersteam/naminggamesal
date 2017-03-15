#!/usr/bin/python

import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import scipy
from scipy import sparse

from . import BaseVocabulary
from . import voc_cache, del_cache




class VocMatrix(BaseVocabulary):

	def __init__(self, M, W, start='empty',**voc_cfg2):
		self._M = M
		self._W = W
		self._size = [self._M,self._W]
		#M = voc_cfg2['M']
		#W = voc_cfg2['W']
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._content=np.matrix(np.zeros((self._M,self._W)))
		if start == 'completed':
			self.complete_empty()

	@del_cache
	def fill(self):
		for i in range(0,self._M):
			for j in range(0,self._W):
				self.add(i,j,1)

	@del_cache
	def complete_empty(self):
		assert len(self.get_known_meanings()) == 0
		for i in range(0,self._M):
			j = self.get_new_unknown_w()
			self.add(i,j,1)

	@voc_cache
	def exists(self,m,w):
		if self._content[m,w] > 0:
			return 1
		else:
			return 0

	def get_value(self,m,w):
		return self._content[m,w]

	def get_content(self):
		return self._content

	def get_size(self):
		return self._size

	def get_random_m(self):
		return random.choice(range(self._M))

	@del_cache
	def add(self,m,w,val=1,context=[]):
		self._content[m,w] = val

	@del_cache
	def rm(self,m,w):
		self._content[m,w] = 0

	def rm_syn(self,m,w):
		for i in self.get_known_words(m=m):
			if i!=w:
				self.rm(m,i)

	def rm_hom(self,m,w):
		for i in self.get_known_meanings(w=w):
			if i!=m:
				self.rm(i,w)

	@voc_cache
	def get_row(self, m):
		return self._content[m,:].reshape((1, self._W))

	@voc_cache
	def get_column(self, w):
		return self._content[:,w].reshape((self._M, 1))

	@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			mat = self._content
		else:
			mat = self.get_row(m)
		coords = self.get_coords(mat, option=option)
		ans = [k[1] for k in coords]
		return sorted(list(set(np.array(ans).reshape(-1,).tolist())))

	@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			mat = self._content
		else:
			mat = self.get_column(w)
		coords = self.get_coords(mat, option=option)
		ans = [k[0] for k in coords]
		return sorted(list(set(np.array(ans).reshape(-1,).tolist())))

	def get_coords(self,mat,option=None):
		nz = mat.nonzero()
		if not nz[0].size:
			return []
		if option is None:
			return self.get_coords_none(mat,nz=nz)
		elif option == 'max':
			return self.get_coords_max(mat,nz=nz)
		elif option == 'min':
			return self.get_coords_min(mat,nz=nz)
		elif option == 'minofmaxw':
			return self.get_coords_minofmaxw(mat,nz=nz)
		elif option == 'minofmaxm':
			return self.get_coords_minofmaxm(mat,nz=nz)

	def get_coords_none(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i],nz[1][i]) for i in range(len(nz[0]))]
		return coords

	def get_coords_max(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = np.argwhere(mat == np.amax(mat[nz]))
		coords = coords.reshape((-1,2))
		return coords

	def get_coords_min(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = np.argwhere(mat == np.amin(mat[nz]))
		coords = coords.reshape((-1,2))
		return coords

	def get_coords_minofmaxw(self,mat,nz=None):
		best_scores = mat.max(axis=0)
		val = np.amin(best_scores)
		coords = np.argwhere(best_scores == val)
		coords = coords.reshape((-1,2))
		return coords

	def get_coords_minofmaxm(self,mat,nz=None):
		best_scores = mat.max(axis=1)
		val = np.amin(best_scores)
		coords = np.argwhere(best_scores == val)
		coords = coords.reshape((-1,2))
		return coords


	@voc_cache
	def get_unknown_words(self, m=None, option=None):
		return sorted(list(set(range(self._W)) - set(self.get_known_words(m=m, option=option))))

	@voc_cache
	def get_unknown_meanings(self, w=None, option=None):
		return sorted(list(set(range(self._M)) - set(self.get_known_meanings(w=w, option=option))))

	def diagnostic(self):
		print self._cache
		print self

	def get_new_unknown_m(self):
		if not len(self.get_known_meanings()) == self._M:
			m = random.choice(self.get_unknown_meanings())
		else:
			#print "tried to get new m but all are known"
			m = self.get_random_known_m(option='minofmaxm')
		return m

	def get_new_unknown_w(self):
		if not len(self.get_known_words()) == self._W:
			w = random.choice(self.get_unknown_words())
		else:
			#print "tried to get new w but all are known"
			w = self.get_random_known_w(option='minofmaxw')
		return w

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

	def visual(self,vtype=None):
		if vtype==None:
			print(self)
		elif vtype=="syn":
			tempmat=np.matrix(np.zeros((self._M,self._W)))
			synvec=[]
			for i in range(0,self._M):
				synvec.append(len(self.get_known_words(i)))
				for j in range(0,self._W):
					tempmat[i,j]=(self._W-synvec[i]+1)*self._content[i,j]
			plt.title("Synonymy")
			plt.xlabel("Words")
			plt.ylabel("Meanings")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=self._W)
		elif vtype=="hom":
			tempmat=np.matrix(np.zeros((self._M,self._W)))
			homvec=[]
			for j in range(0,self._W):
				homvec.append(len(self.get_known_meanings(j)))
				for i in range(0,self._M):
					tempmat[i,j]=(self._M-homvec[j]+1)*self._content[i,j]
			plt.title("Homonymy")
			plt.xlabel("Words")
			plt.ylabel("Meanings")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=self._M)






class VocSparseMatrix(VocMatrix):
	voctype="sparse_matrix"

	@voc_cache
	def get_content(self):
		return self._content.todense()

	@voc_cache
	def get_row(self, m):
		return self._content.getrow(m)

	@voc_cache
	def get_column(self, w):
		return self._content.getcol(w)

	def get_coords(self,mat,option=None):
		mat.eliminate_zeros()
		return VocMatrix.get_coords(self,mat,option=option)


class VocLiLMatrix(VocSparseMatrix):
	voctype="lil_matrix"

	def __init__(self,M,W,start='empty',**voc_cfg2):
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._M = M
		self._W = W
		self._content = sparse.lil_matrix((self._M,self._W))
		if start == 'completed':
			self.complete_empty()

	@voc_cache
	def get_column(self, w):
		return self._content.getcol(w).tolil()

	def get_coords_none(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords =[]
		for i in range(len(mat.rows)):
			coords += [(i,mat.rows[i][j]) for j in range(len(mat.rows[i]))]
		return coords

	def get_coords_max(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		mat_max = np.amax(mat.data.max())
		coords =[]
		for i in range(len(mat.rows)):
			coords += [(i,mat.rows[i][j]) for j in range(len(mat.rows[i])) if mat.data[i][j] == mat_max]
		return coords

	def get_coords_min(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		mat_min = np.amin(mat.data.min())
		coords =[]
		for i in range(len(mat.rows)):
			coords += [(i,mat.rows[i][j]) for j in range(len(mat.rows[i])) if mat.data[i][j] == mat_min]
		return coords


class VocCSRMatrix(VocSparseMatrix):
	voctype="csr_matrix"

	def __init__(self,M,W,start='empty',**voc_cfg2):
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._M = M
		self._W = W
		self._content = sparse.csr_matrix((self._M,self._W))

		if start == 'completed':
			self.complete_empty()

	def get_coords_none(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i],nz[1][i]) for i in range(len(nz[0]))] #tolist??
		return coords

	def get_coords_max(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i[0]],nz[1][i[0]]) for i in np.argwhere(mat.data == mat.data.max()) if mat.data.any()]
		return coords

	def get_coords_min(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i[0]],nz[1][i[0]]) for i in np.argwhere(mat.data == mat.data.min()) if mat.data.any()]
		return coords

	def get_coords_minofmaxm(self,mat,nz=None):
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
		return coords

	def get_coords_minofmaxw(self,mat,nz=None):
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
		return coords


class VocCSRMatrixImproved(VocCSRMatrix):
	voctype="csr_matrix_improved"

	def __init__(self,M,W,**voc_cfg2):
		VocCSRMatrix.__init__(self,M,W,**voc_cfg2)
		self._content.tocoo = self.convert_to_coo


	def convert_to_coo(self,copy=True):
		if 'coo' not in self._cache.keys():
			self._cache['coo'] = sparse.csr_matrix.tocoo(self._content)
		return self._cache['coo']

	def __getstate__(self):
		del self._content.tocoo
		out_dict = self.__dict__.copy()
		out_dict['_content'] = copy.deepcopy(self._content)
		self._content.tocoo = self.convert_to_coo
		return out_dict

	def __setstate__(self, in_dict):
		self.__dict__.update(in_dict)
		self._content.tocoo = self.convert_to_coo



class VocCSCMatrix(VocCSRMatrix):
	voctype="csc_matrix"

	def __init__(self,M,W,start='empty',**voc_cfg2):
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._M = M
		self._W = W
		self._content = sparse.csc_matrix((self._M,self._W))

		if start == 'completed':
			self.complete_empty()



class VocDOKMatrix(VocSparseMatrix):
	voctype="dok_matrix"

	def __init__(self,M,W,start='empty',**voc_cfg2):
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._M = M
		self._W = W
		self._content = sparse.dok_matrix((self._M,self._W))

		if start == 'completed':
			self.complete_empty()

	def get_coords(self, mat, option=None):
		if option is None:
			coords = mat.keys()
		elif option == 'min':
			mat_min = min(mat.values())
			coords = [k for k,v in mat.iteritems() if v == mat_min]
		elif option == 'max':
			mat_max = max(mat.values())
			coords = [k for k,v in mat.iteritems() if v == mat_max]
		return coords


	def __getstate__(self):
		out_dict = self.__dict__.copy()
		a = {}
		a.update(out_dict['_content'])
		out_dict['_content_dict'] = out_dict['_content'].__dict__
		out_dict['_content'] = a
		return out_dict

	def __setstate__(self, in_dict):
		mat = sparse.dok_matrix((in_dict['_M'],in_dict['_W']))
		mat.__dict__ = in_dict['_content_dict']
		mat.update(in_dict['_content'])
		del in_dict['_content_dict']
		in_dict['_content'] = mat
		self.__dict__ = in_dict
