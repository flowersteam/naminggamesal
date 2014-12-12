#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np

temp=np.matrix(np.zeros((3,3)))
temp2=np.matrix(np.zeros((3,3)))

temp[1,1]=2
temp[2,1]=3

print temp 
print temp*temp
print np.multiply(temp,temp)