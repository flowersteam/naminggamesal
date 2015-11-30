#!/usr/bin/python

import random
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import sparse

from . import BaseVocabulary
from . import voc_cache, del_cache




class VocMatrix(BaseVocabulary):

	def __init__(self, M, W, **voc_cfg2):
		self._M = M
		self._W = W
		self._size = [self._M,self._W]
		#M = voc_cfg2['M']
		#W = voc_cfg2['W']
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._content=np.matrix(np.zeros((self._M,self._W)))

	@voc_cache
	def exists(self,m,w):
		if self._content[m,w] > 0:
			return 1
		else:
			return 0

	def get_content(self):
		return self._content

	def get_size(self):
		return self._size

	@del_cache
	def add(self,m,w,val):
		self._content[m,w] = val

	@del_cache
	def rm(self,m,w):
		self._content[m,w] = 0

	@del_cache
	def rm_syn(self,m,w):
		for i in range(0,self._W):
			if i!=w:
				self._content[m,i] = 0

	@del_cache
	def rm_hom(self,m,w):
		for i in range(0,self._M):
			if i!=m:
				self._content[i,w] = 0

	@voc_cache
	def get_row(self, m):
		return self._content[m,:]

	@voc_cache
	def get_column(self, w):
		return self._content[:,w]

	@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			mat = self._content
		else:
			mat = self.get_row(m)
		nz = mat.nonzero()
		if not nz[0].size:
			ans = []
		elif option is None:
			ans = nz[1]
		elif option == 'max':
			coords = np.argwhere(mat == np.amax(mat))
			ans = [k[0,1] for k in coords]
		elif option == 'min':
			coords = np.argwhere(mat == np.amin(mat))
			ans = [k[0,1] for k in coords]
		else:
			raise ValueError('Unknown option')
		return sorted(list(set(np.array(ans).reshape(-1,).tolist())))

	@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			mat = self._content
		else:
			mat = self.get_column(w)
		nz = mat.nonzero()
		if not nz[0].size:
			ans = []
		elif option is None:
			ans = nz[0]
		elif option == 'max':
			coords = np.argwhere(mat == np.amax(mat))
			ans = [k[0,0] for k in coords]
		elif option == 'min':
			coords = np.argwhere(mat == np.amin(mat))
			ans = [k[0,0] for k in coords]
		else:
			raise ValueError("Unknown option")
		return sorted(list(set(np.array(ans).reshape(-1,).tolist())))

	@voc_cache
	def get_unknown_words(self, m=None, option=None):
		return sorted(list(set(range(self._W)) - set(self.get_known_words(m=m, option=option))))

	@voc_cache
	def get_unknown_meanings(self, w=None, option=None):
		return sorted(list(set(range(self._M)) - set(self.get_known_meanings(w=w, option=option))))

	def get_new_unknown_m(self, option='min'):
		try:
			m = random.choice(self.get_unknown_meanings())
		except IndexError:
			print "tried to get new m but all are known"
			m = self.get_random_known_m(option=option)
		return m

	def get_new_unknown_w(self, option='min'):
		try:
			w = random.choice(self.get_unknown_words())
		except IndexError:
			print "tried to get new w but all are known"
			w = self.get_random_known_w(option=option)
		return w

	def get_random_known_m(self,w=None, option='max'):
		try:
			print self.get_known_meanings(w=w, option=option)
			m = random.choice(self.get_known_meanings(w=w, option=option))
		except IndexError:
			print "tried to get known m but none are known"
			m = self.get_new_unknown_m()
		return m

	def get_random_known_w(self,m=None, option='max'):
		try:
			print self.get_known_words(m=m, option=option)
			w = random.choice(self.get_known_words(m=m, option=option))
		except IndexError:
			print "tried to get known w but none are known"
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

	def __init__(self,M,W,**voc_cfg2):
		super(VocMatrix,self).__init__(**voc_cfg2)
		self._M = M
		self._W = W
		self._content = sparse.csr_matrix((self._M,self._W))

	@voc_cache
	def get_content(self):
		return self._content.todense()

	@voc_cache
	def get_row(self, m):
		return self._content.getrow(m)

	@voc_cache
	def get_column(self, w):
		return self._content.getcol(w)

#	def __getstate__(self):
#		out_dict = self.__dict__.copy()
#		out_dict['_content'] = self._content.tocoo()
#		return out_dict
#
#	def __setstate__(self, in_dict):
#		self.__dict__.update(in_dict)
#		self._content = self._content.todok()

	@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is None:
			mat = self._content
		else:
			mat = self.get_row(m)
		nz = mat.nonzero()
		if not list(nz[0]):
			ans = []
		elif option is None:
			ans = nz[0]
		elif option == 'max':
			coords = [(nz[0][i],nz[1][i]) for i in np.argwhere(mat.data == mat.data.max())]
			ans = [j for (i,j) in [tuple(k) for k in coords]]
		elif option == 'min':
			coords = [(nz[0][i],nz[1][i]) for i in np.argwhere(mat.data == mat.data.min())]
			ans = [j for (i,j) in [tuple(k) for k in coords]]
		else:
			raise ValueError('Unknown option')
		return sorted(list(set(np.array(ans).reshape(-1,).tolist())))

	@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is None:
			mat = self._content
		else:
			mat = self.get_column(w)#self._content[:,w]
		nz = mat.nonzero()
		if not list(nz[0]):
			ans = []
		elif option is None:
			ans = nz[1]
		elif option == 'max':
			coords = [(nz[0][i],nz[1][i]) for i in np.argwhere(mat.data == mat.data.max())]
			ans = [i for (i,j) in [tuple(k) for k in coords]]
		elif option == 'min':
			coords = [(nz[0][i],nz[1][i]) for i in np.argwhere(mat.data == mat.data.min())]
			ans = [i for (i,j) in [tuple(k) for k in coords]]
		else:
			raise ValueError("Unknown option")
		return sorted(list(set(np.array(ans).reshape(-1,).tolist())))
