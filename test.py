#!/usr/bin/python
# -*- coding: latin-1 -*-
# import ngsimu
# import time

# M=10
# W=20
# N=20
# steps=300

# testmat=ngsimu.Experiment("matrix","naive",M,W,N,1)
# testspa=ngsimu.Experiment("matrix","naive",M,W,N,1)

# tmat=-time.time()
# for i in range(0,steps):
# 	testmat.continue_exp()
# 	print i
# tmat+=time.time()

# tsp=-time.time()
# for i in range(0,steps):
# 	testspa.continue_exp()
# 	print i
# tsp+=time.time()

# print "tmat:%d"%tmat
# print "tsp:%d"%tsp

import matplotlib.pyplot as plt
import numpy as np 
M=1000
W=M
def G(m):
	return -np.log2(W-m)

def Pp(m):
	return (M-m)*(W-m)/float(M*W)


def Pm(m):
	return (m*m-m)/float(M*W)

def gain(m):
	return Pp(m)*G(m)-Pm(m)*G(m-1)

Y=[]
Y2=[]

for i in range(2,M-2):
	Y.append(gain(i+1)+G(i))
	Y2.append(gain(i))

plt.ion()
plt.plot(range(2,M-2),Y)
plt.plot(range(2,M-2),Y2)
plt.show()
