#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
from scipy import sparse

class Vocabulary(object):

	def __new__(cls,voctype,M,W):
		if voctype=="matrix":
			return object.__new__(VocMatrix,M,W)
		elif voctype=="sparse":
			return object.__new__(VocSparse,M,W)
		else:
			print "type de vocabulaire non existant"

	def __init__(self,voctype,M,W):
		self._M=M
		self._W=W
		self._size=[M,W]

	def fill(self):
		for i in range(0,self._M):
			for j in range(0,self._W):
				self.add(i,j,1)

	def affiche(self):
		print(self.get_content())

	def get_voctype(self):
		return _voctype

	def get_M(self):
		return self._M

	def get_W(self):
		return self._W


class VocMatrix(Vocabulary):
	_voctype="matrix"

	def __init__(self,voctype,M,W):
		super(VocMatrix,self).__init__(voctype,M,W)
		self._content=np.matrix(np.zeros((self._M,self._W)))

	def get_known_words(self,*args):
		templ=[]
		if len(args)==0:
			for w in range(0,self._W):
				tempbool=1
				for m in range(0,self._M):
					tempbool=tempbool*self.exists(m,w)
				if tempbool==1:
					templ.append(w)
		else:
			for w in range(0,self._W):
				tempbool=1
				tempbool=tempbool*self.exists(args[0],w)
				if tempbool==1:
					templ.append(w)
		return templ

	def get_known_meanings(self,*args):
		templ=[]
		if len(args)==0:
			for m in range(0,self._M):
				tempbool=1
				for w in range(0,self._W):
					tempbool=tempbool*self.exists(m,w)
				if tempbool==1:
					templ.append(m)
		else:
			for m in range(0,self._M):
				tempbool=1
				tempbool=tempbool*self.exists(m,args[0])
				if tempbool==1:
					templ.append(m)
		return templ

	def exists(self,m,w):
		if self._content[m,w]>0:
			return 1
		else:
			return 0

	def get_content(self):
		return self._content

	def get_size(self):
		return self._size

	def add(self,m,w,val):
		self._content[m,w]=val

	def rm(self,m,w):
		self._content[m,w]=0

	def rm_syn(self,m,w):
		for i in range(0,self._W):
			if i!=w:
				self._content[m,i]=0

	def rm_hom(self,m,w):
		for i in range(0,self._M):
			if i!=m:
				self._content[i,w]=0


class VocSparse(VocMatrix):
	voctype="sparse"
	
	def __init__(self,voctype,M,W):
		super(VocMatrix,self).__init__(voctype,M,W)
		self._content=sparse.lil_matrix((M,W))


	def get_known_words(self,*args):
		templ=[]
		if len(args)==0:
			for w in range(0,self._W):
				tempbool=1
				for m in range(0,self._M):
					tempbool=tempbool*self.exists(m,w)
				if tempbool==1:
					templ.append(w)
		else:
			for w in range(0,self._W):
				tempbool=1
				tempbool=tempbool*self.exists(args[0],w)
				if tempbool==1:
					templ.append(w)
		return templ

	def get_known_meanings(self,*args):
		templ=[]
		if len(args)==0:
			for m in range(0,self._M):
				tempbool=1
				for w in range(0,self._W):
					tempbool=tempbool*self.exists(m,w)
				if tempbool==1:
					templ.append(m)
		else:
			for m in range(0,self._M):
				tempbool=1
				tempbool=tempbool*self.exists(m,args[0])
				if tempbool==1:
					templ.append(m)
		return templ

	def exists(self,m,w):
		if self._content[m,w]>0:
			return 1
		else:
			return 0

	def get_content(self):
		return self._content

	def get_size(self):
		return self._size

	def add(self,m,w,val):
		self._content[m,w]=val

	def rm(self,m,w):
		self._content[m,w]=0

	def rm_syn(self,m,w):
		for i in range(0,self._W):
			if i!=w:
				self._content[m,i]=0

	def rm_hom(self,m,w):
		for i in range(0,self._M):
			if i!=m:
				self._content[i,w]=0

	def get_content(self):
		return self._content.todense()


# if __name__ == "__main__":
# 	print "main"

#	with open('donnees', 'wb') as fichier:
#		mon_pickler = pickle.Pickler(fichier)
#		mon_pickler.dump(testpop2)

#	with open('donnees', 'rb') as fichier:
#		mon_depickler = pickle.Unpickler(fichier)
#		pop_recupere = mon_depickler.load()