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

import ngmeth
import time
import matplotlib.pyplot as plt

M=20
N=20
W=20
strat="naive"
voc="sparse"
Treal=400
step=10
T=Treal/step
iterr=1

def generate():

	for i in range(0,iterr):
		tempstr="iterr:"+str(i)+"/"+str(iterr)
		tempsimu=ngmeth.Experiment(voc,strat,M,W,N,1)
		for j in range(0,T):
			tempstr=tempstr+" T:"+str(j)+"/"+str(T)
			tempsimu.continue_exp()
		#tempsimu.save("tempsimdir/tmp"+str(int(time.time()))+".tmp")
	return tempsimu 

def plot(simu):
	data=ngmeth.Nlinkmoyenexpe(simu)
	plt.plot(data[0])
	plt.show()

print "test"

print __name__