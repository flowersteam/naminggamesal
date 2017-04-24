import random
import numpy as np
import copy
import networkx as nx

from . import BaseVocabulary, get_vocabulary
from . import voc_cache, del_cache



class VocGraph(BaseVocabulary):

	def __init__(self, subvoc_cfg):
		self.subvoc = get_vocabulary(**subvoc_cfg)
		self.graph = nx.Graph()#create graph

	def __getattr__(self, name):
		return getattr(self.subvoc, name)

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
			return self.graph.adjacent(m) - set(self.get_known_meanings())#get neighbors of m, set substract
		else:
			for m1 in self.get_known_meanings():
				ans_set += self.get_adjacent_possible(m=m1)

