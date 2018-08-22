
import numpy as np
import sys

if sys.version_info.major == 3:
	xrange = range

def t_1inv(N):
	return 2+(np.log(N-2)/(np.log(N)-np.log(N-1)))

def a_eq(N):
	return 1./8*(7*N-4-np.sqrt(17*N**2-24*N+16))

def c_eq(N):
	return N - 2*a_eq(N)

def inv2_eps(N):
	eps0 = 1.
	return np.log(2.*a_eq(N)/eps0)/np.log(1.+(c_eq(N)/(2*N*(N-1))))

def inv2_c(N):
	def iter_c(x):
		return x - x*((N-2.-3.*x)/(N*(N-1)))
	c = c_eq(N)
	if N < 19:
		return 1 #Computation issue for N <19
	else:
		for i in xrange(10**10):
			c = iter_c(c)
			if c <= 1.:
				if c == 1.:
					return i + 1
				else:
					return i
		raise ValueError('Computation too long, cannot get convergence time')

def t_2inv(N):
	return inv2_eps(N) + inv2_c(N)

def minexplo_per_ag(M,N):
	def iter_M(x):
		return x * ((x-1.)/x)**(N/2.)
	m = M
	for i in xrange(10**10):
		m = iter_M(m)
		if m <= 1.:
			if m == 1.:
				return i + 1
			else:
				return i
	raise ValueError('Computation too long, cannot get convergence time')

def extra_inv(M,N):
	return N*minexplo_per_ag(M=M,N=N) - M


