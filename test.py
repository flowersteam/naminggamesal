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
import sys
from blessings import Terminal
from time import sleep
import multiprocessing

import my_functions

for i in range(20):
	my_functions.print_on_line("TESTTEST______TESTTESTTEST",18)
	print str(i)*30