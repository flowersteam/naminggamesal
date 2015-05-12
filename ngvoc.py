#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
from scipy import sparse
import random

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


	def get_known_words(self,*args):
		templ=[]
		if len(args)==0:
			for w in range(0,self._W):
				tempbool=1
				for m in range(0,self._M):
					tempbool=tempbool*(1-self.exists(m,w))
				if tempbool==0:
					templ.append(w)
		else:
			for w in range(0,self._W):
				tempbool=1
				tempbool=tempbool*(1-self.exists(args[0],w))
				if tempbool==0:
					templ.append(w)
		return templ

	def get_known_meanings(self,*args):
		templ=[]
		if len(args)==0:
			for m in range(0,self._M):
				tempbool=1
				for w in range(0,self._W):
					tempbool=tempbool*(1-self.exists(m,w))
				if tempbool==0:
					templ.append(m)
		else:
			for m in range(0,self._M):
				tempbool=1
				tempbool=tempbool*(1-self.exists(m,args[0]))
				if tempbool==0:
					templ.append(m)
		return templ


	def get_unknown_words(self,*args):
		templ=[]
		if len(args)==0:
			for w in range(0,self._W):
				tempbool=1
				for m in range(0,self._M):
					tempbool=tempbool*(1-self.exists(m,w))
				if tempbool==1:
					templ.append(w)
		else:
			for w in range(0,self._W):
				tempbool=1
				tempbool=tempbool*(1-self.exists(args[0],w))
				if tempbool==1:
					templ.append(w)
		return templ

	def get_unknown_meanings(self,*args):
		templ=[]
		if len(args)==0:
			for m in range(0,self._M):
				tempbool=1
				for w in range(0,self._W):
					tempbool=tempbool*(1-self.exists(m,w))
				if tempbool==1:
					templ.append(m)
		else:
			for m in range(0,self._M):
				tempbool=1
				tempbool=tempbool*(1-self.exists(m,args[0]))
				if tempbool==1:
					templ.append(m)
		return templ

	def get_new_unknown_m(self):
		if len(self.get_unknown_meanings())==0:
			print "tried to get new m but all are known"
			return self.get_random_known_m()
		tempindexm=random.randint(0,len(self.get_unknown_meanings())-1)
		m=self.get_unknown_meanings()[tempindexm]
		return m

	def get_new_unknown_w(self):
		if len(self.get_unknown_words())==0:
			print "tried to get new w but all are known"
			return self.get_random_known_w()
		tempindexw=random.randint(0,len(self.get_unknown_words())-1)
		w=self.get_unknown_words()[tempindexw]
		return w


	def get_random_known_m(self,*args):
		if len(self.get_known_meanings())==0:
			print "tried to get known m but none are known"
			return self.get_new_unknown_m()
		tempindexm=random.randint(0,len(self.get_known_meanings(*args))-1)
		m=self.get_known_meanings(*args)[tempindexm]
		return m

	def get_random_known_w(self,*args):
		if len(self.get_known_words())==0:
			print "tried to get known w but none are known"
			return self.get_new_unknown_w()
		tempindexw=random.randint(0,len(self.get_known_words(*args))-1)
		w=self.get_known_words(*args)[tempindexw]
		return w





#####################################"" MATRICES CREUSES #############################################


class VocSparse(VocMatrix):
	voctype="sparse"
	
	def __init__(self,voctype,M,W):
		super(VocMatrix,self).__init__(voctype,M,W)
		self._content=sparse.lil_matrix((M,W))

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