#!/usr/bin/python
# -*- coding: latin-1 -*-
import numpy as np
test=np.zeros(7)
test[3]=1
test[0]=1
test[5]=1
print test
def nemenonnul(n,l):
	temp=0
	for i in range(0,len(l)):
		print i
		if l[i]!=0:
			print "print"
			temp+=1
		if temp==n:
			return i

i=nemenonnul(3,test)
print i