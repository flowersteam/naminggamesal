import random
import numpy as np
import copy
import networkx as nx

from . import BaseVocabulary, get_vocabulary
from . import voc_cache, del_cache



class VocGraph(BaseVocabulary):

	def __init__(self, subvoc_cfg, env=None):
		self.subvoc = get_vocabulary(**subvoc_cfg)
		self._content = self.subvoc._content
		self._cache = self.subvoc._cache
		if hasattr(self.subvoc,'_M'):
			self._M = self.subvoc._M
		if hasattr(self.subvoc,'_W'):
			self._W = self.subvoc._W
		self.init_graph(env=env)
		self.set_core_meanings(env=env)

	def set_core_meanings(self,env):
		if env is None:
			self.core_meanings = [0]
		else:
			self.core_meanings = env.core_meanings

	def init_graph(self,env):
		#self.graph = nx.Graph()#create graph
		#self.graph.add_nodes_from(range(self.subvoc._M))
		if env is None:
			self.graph = nx.complete_graph(self.subvoc._M)
		else:
			self.graph = env.meaning_graph


	def get_new_unknown_m(self):
		if len(self.get_adjacent_possible()) > 0:
			m = random.choice(self.get_adjacent_possible())
		else:
			#print "tried to get new m but all are known"
			m = self.get_random_known_m(option='minofmaxm')
		return m

	@voc_cache
	def get_adjacent_possible(self,m=None):
		if m is not None:
			return list(set(self.graph.neighbors(m)) - set(self.get_known_meanings()))
		else:
			ans_set = set(self.core_meanings) - set(self.get_known_meanings())
			for m1 in self.get_known_meanings():
				ans_set = ans_set | set(self.get_adjacent_possible(m=m1))
			return list(ans_set)

	@voc_cache
	def get_accessible_meanings(self):
		return self.get_known_meanings() + self.get_adjacent_possible()

	def draw(self):
		nx.draw(self.graph)




	def fill(self):
		return self.subvoc.fill()

	def complete_empty(self):
		return self.subvoc.complete_empty()

	def exists(self,m,w):
		return self.subvoc.exists(m,w)

	def get_value(self,m,w):
		return self.subvoc.get_value(m,w)

	def get_content(self):
		return self.subvoc.get_content()

	def get_size(self):
		return self.subvoc.get_size()

	def get_random_m(self):
		return self.subvoc.get_random_m()

	def add(self,m,w,val=1,context=[]):
		return self.subvoc.add(m=m,w=w,val=val,context=context)

	def rm(self,m,w):
		return self.subvoc.rm(m=m,w=w)

	def rm_syn(self,m,w):
		return self.subvoc.rm_syn(m=m,w=w)

	def rm_hom(self,m,w):
		return self.subvoc.rm_hom(m=m,w=w)

	def get_row(self, m):
		return self.subvoc.get_row(m=m)

	def get_column(self, w):
		return self.subvoc.get_column(w=w)

	def get_known_words(self,m=None,option=None):
		return self.subvoc.get_known_words(m=m,option=option)

	def get_known_meanings(self,w=None,option=None):
		return self.subvoc.get_known_meanings(w=w,option=option)

	def get_coords(self,mat,option=None):
		return self.subvoc.get_coords(mat=mat,option=option)

	def get_coords_none(self,mat,nz=None):
		return self.subvoc.get_coords_none(mat=mat,nz=nz)

	def get_coords_max(self,mat,nz=None):
		return self.subvoc.get_coords_max(mat=mat,nz=nz)

	def get_coords_min(self,mat,nz=None):
		return self.subvoc.get_coords_min(mat=mat,nz=nz)

	def get_coords_minofmaxw(self,mat,nz=None):
		return self.subvoc.get_coords_minofmaxw(mat=mat,nz=nz)

	def get_coords_minofmaxm(self,mat,nz=None):
		return self.subvoc.get_coords_minofmaxm(mat=mat,nz=nz)

	def get_unknown_words(self, m=None, option=None):
		return self.subvoc.get_unknown_words(m=m,option=option)

	def get_unknown_meanings(self, w=None, option=None):
		return self.subvoc.get_unknown_meanings(w=w,option=option)

	def diagnostic(self):
		return self.subvoc.diagnostic()

	def get_new_unknown_w(self):
		return self.subvoc.get_new_unknown_w()

	def get_random_known_m(self,w=None, option='max'):
		return self.subvoc.get_random_known_m(w=w,option=option)

	def get_random_known_w(self,m=None, option='max'):
		return self.subvoc.get_random_known_w(m=m,option=option)

	def visual(self,vtype=None):
		return self.subvoc.visual(vtype=vtype)






class BarabasiAlbertVocGraph(VocGraph):

	def init_graph(self,env):
		self.graph = nx.barabasi_albert_graph(self.subvoc._M,5)
