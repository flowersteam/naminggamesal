#!/usr/bin/python

from . import Evolution
import random
import numpy as np
import networkx as nx

##########
class Replace(Evolution):
	def __init__(self,rate=1):
		self.count = 0
		self.rate = rate

	def step(self,pop):
		if self.count == self.rate-1:
			pop.rm_agent()
			pop.add_new_agent()
			self.count = 0
		else:
			self.count += 1

