#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
from scipy import sparse
temp=np.matrix(np.zeros((3,3)))
temp2=sparse.lil_matrix((3,3))
print temp2.todense()

temp2[1,1]=2
temp2[2,1]=3

print temp2.todense()
print temp2.todense()*temp2.todense()
print np.multiply(temp2,temp2).todense()
print temp2.multiply(temp2).todense()

import time
import progressbar
progress = progressbar.ProgressBar()
for i in progress(range(80)):
  time.sleep(0.01)