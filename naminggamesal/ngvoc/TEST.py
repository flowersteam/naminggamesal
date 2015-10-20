#!/usr/bin/python

import random
import numpy as np
import matplotlib.pyplot as plt

from .matrix import VocMatrix

class VocTest(VocMatrix):
	voctype="test"

	def __init__(self,number, testkey, **voc_cfg2):
		super(VocTest,self).__init__(M=number/2, W=15, **voc_cfg2)
		self.key = testkey

	def test(self):
		print 'testkey:{}'.format(str(self.key))
