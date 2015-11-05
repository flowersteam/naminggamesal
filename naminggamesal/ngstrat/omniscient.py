#!/usr/bin/python

from .naive import StratNaive
import random
import numpy as np



##################################### STRATEGIE SUCCESS THRESHOLD########################################
class StratOmniscient(StratNaive):

	def pick_m(self,voc,mem):
		return self.pick_mw(voc,mem)[0]

	def hearer_pick_m(self,voc,mem):
		return self.pick_m(voc, mem)

	def update_memory(self,ms,w,mh,voc,mem,role):
		pass

	def init_memory(self,voc):
		return {}

	def pick_mw(self,voc,mem):
		matrix = np.multiply(np.multiply((np.ones_like(mem['hearer']) - mem['hearer']), mem['pop']), voc.get_content())
		coords = []
		max_val = 0
		for i in range(matrix.shape[0]):
			for j in range(matrix.shape[1]):
				val = matrix[i,j]
				if (not val == 1):
					if val > max_val:
						coords = [(i,j)]
						max_val = val
					elif val == max_val:
						coords.append((i,j))
		if not coords or max_val ==0:
			m = voc.get_new_unknown_m()
			w = self.pick_w(voc=voc,mem=mem,m=m)
			return (m, w)
		else:
			r = random.randint(0,len(coords)-1)
			return coords[r]


