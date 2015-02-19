#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
from scipy import sparse

class simu:
	def affiche(self):
		print(self.content)



class vocsparse(vocabulary):
	typevoc="sparse"
	def __init__(self,M,W):
		self.M=M
		self.W=W
		self.size=[M,W]