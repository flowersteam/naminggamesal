import numpy as np
import math
from .conv_utils import iter_M

def m_limit_theorique(M,W):
	return (-((M+W-1.)/2.)+math.sqrt((M+W-1.)**2/4.+2.*M*W))/2.

def decvec_from_MW(M,W):
	decvec=[]
	m=m_limit_theorique(M,W)
	for i in range(0,M+1):
		if i<=m:
			decvec.append(1)
		else:
			decvec.append(0)
	return decvec



def decvectest_from_MW(M,W):
	decvec=[]
	m0=0
	for i in range(0,M+1):
		dm=i-m0
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		print(pp)
		print(pm)
		print(" ")
		if pm<=pp:
			decvec.append(1)
		else:
			decvec.append(0)
	return decvec

def decvec2_from_MW(M,W):
	decvec=[]
	m0=0
	for i in range(0,M+1):
		dm=i-m0
		pp=(M-i)/float(M)*(W-i)/float(W-dm)
		pm=m0/float(M)*(m0-1.)/float(W-dm)
		print(pp)
		print(pm)
		print(" ")
		if pm<=pp:
			decvec.append(1)
			m0+=1
		else:
			decvec.append(0)
	return decvec


def decvec3_from_MW(M,W):
	decvec=[]
	for i in range(0,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		if pm*Gm<=pp*Gp:
			decvec.append(1)
		else:
			decvec.append(0)
	decvec.append(0)
	return decvec


def decvec3_softmax_from_MW(M,W,Temp):
	decvec=[]
	for i in range(0,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(-pm*Gm/Temp)
		decvec.append(P1/(P1+P2))
	decvec.append(0)
	return decvec


def decvec4_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P1/(P1+P2)
		if np.isnan(p):
			if pm*Gm<=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvec5_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(W-i)/float(W)
		pm=(i*(i-1)+(M-i)*(i-1))/float(M*W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P2/(P1+P2)
		if np.isnan(p):
			if pm*Gm>=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvectest_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(W-i)/float(W)
		pm=(i*(i-1)+(M-i)*(i-1))/float(M*W)
		Gp=np.log2(W-i)
		Gm=-np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P2/(P1+P2)
		if np.isnan(p):
			if pm*Gm>=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvec_full_explo(M,W):
	decvec = [1.]
	for i in range(1,M):
		decvec.append(1.)
	decvec.append(0.)


def decvec_full_teach(M,W):
	decvec = [1.]
	for i in range(1,M):
		decvec.append(0.)
	decvec.append(0.)


def decvec_chunks_from_MW(M,W,N,Temp=0.01):
	decvec=np.ones((M+1))*Temp
	decvec[0] = 1.
	decvec[-1] = 0.
	MM = M
	while MM > 1:
		decvec[M-MM] = 1.
		MM = int(iter_M(x=MM,N=N))
	return decvec
