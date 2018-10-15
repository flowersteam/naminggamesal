
import numpy as np
import sys

from tconv_values import tc_dict

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
		for i in xrange(10**8):
			c = iter_c(c)
			if c <= 1.:
				if c == 1.:
					return i + 1
				else:
					return i
		raise ValueError('Computation too long, cannot get convergence time')

def t_2inv(N):
	return inv2_eps(N) + inv2_c(N)

def iter_M(x,N):
	return x * ((x-1.)/x)**(N/2.)

def minexplo_per_ag(M,N):
	m = M
	for i in xrange(10**6):
		m = iter_M(m,N)
		if m <= 1.:
			if m == 1.:
				return (i + 1)/2.
			else:
				return i/2.
	raise ValueError('Computation too long, cannot get convergence time')

def nchunks(M,N):
	m = M
	for i in xrange(10**10):
		m = iter_M(m,N)
		if m <= 1.:
			if m == 1.:
				ans = i#(i + 1)
			else:
				ans = i
			return max(ans,1)
	raise ValueError('Computation too long, cannot get convergence time')

def extra_inv(M,N):
	return N*minexplo_per_ag(M=M,N=N) - M

def tconv_naive(N):
	if N>10**6:
		raise ValueError('Convergence time for population size of more than a million is not known exactly.')
	elif N>100:
		return (2.3+np.sin(1.+0.4*np.log(N)))*N**1.5
	else:
		return tc_dict[N]

def tconv_optimal(M,N,ninv=None):
	if ninv is None:
		ninv = N/2.
	return M*(tconv_naive(N=int(2*ninv/M)) + N*np.log(N))

def ninv_optimal(M,N):
	return max(M,N/2.)

def memmax_optimal(M,N):
	return M


def perf1(tc,M,N):
	return tconv_optimal(N=N,M=M)*1./tc

def perf2(srtheo_vec,t_vec,M,N):
	t_n = tconv_optimal(M=M,N=N)
	srtheo_vec = list(srtheo_vec)
	srtheo_vec.reverse()
	t_vec = list(t_vec)
	t_vec.reverse()
	for sr,t in zip(srtheo_vec,t_vec):
		if t <= t_n:
			return sr

def perf1_ninv(ninv,M,N):
	return ninv_optimal(N=N,M=M)*1./ninv

def perf1_tconvninv(ninv,M,N):
	return tconv_optimal(N=N,M=M,ninv=ninv)*1./ninv

def perf2_tconvninv(srtheo_vec,t_vec,M,N,ninv):
	t_n = tconv_optimal(M=M,N=N,ninv=ninv)
	srtheo_vec = list(srtheo_vec)
	srtheo_vec.reverse()
	t_vec = list(t_vec)
	t_vec.reverse()
	for sr,t in zip(srtheo_vec,t_vec):
		if t <= t_n:
			return sr


def perf1_memmax(memmax,M,N):
	return memax_optimal(N=N,M=M)*1./memmax

if __name__ == '__main__':
	# scale_vec = [10,20,50,100,500,1000,2000,5000,10000,20000,50000,100000]
	# import matplotlib.pyplot as plt
	# for N in [10,100,1000,10000,100000]:
	# 	Y = [minexplo_per_ag(M,N)/M for M in scale_vec]
	# 	plt.plot(scale_vec,Y,label='N='+str(N))
	# plt.legend()
	# plt.xlabel('M')
	# plt.show()
	# for M in [10,100,1000,10000,100000]:
	# 	Y = [minexplo_per_ag(M,N) for N in scale_vec]
	# 	plt.plot(scale_vec,Y,label='M='+str(M))
	# plt.xlabel('N')
	# plt.legend()
	# plt.show()
	# for coeff in [0.1,0.5,1.,2.,10.]:
	# 	Y = [minexplo_per_ag(coeff*N,N) for N in scale_vec]
	# 	plt.plot(scale_vec,Y,label='M='+str(coeff)+'*N')
	# plt.xlabel('N')
	# plt.legend()
	# plt.show()
	# for coeff in [0.1,0.5,1.,2.,10.]:
	# 	Y = [(minexplo_per_ag(coeff*N,N)*N)-N*coeff for N in scale_vec]
	# 	plt.plot(scale_vec,Y,label='M='+str(coeff)+'*N')
	# plt.xlabel('N')
	# plt.legend()
	# plt.show()
	N_l = [10,100,1000]
	Nc_l = [0.2,0.5,0.7,0.8,0.95,1.,2.,5,10]
	M_l = [100,1000,10000]
	for M in M_l:
		for Nc in Nc_l:
			N = int(Nc*M)
			val = int(2*M/N)+ 1
			print('N',N,'M',M,'2M/N+1',val,'nch',nchunks(M,N))
			print(val-nchunks(M,N))
	print('tab')
	for Nc in Nc_l:
		for M in M_l:
			N = int(Nc*M)
			val = int(2*M/N)+1
			print(N,'&',M,'&',val,'&',nchunks(M,N), '\\\\')
			# print(val-nchunks(M,N))


	print('tab')
	for Nc in Nc_l:
		for M in M_l:
			N = int(Nc*M)
			val = int(2*M/N)+1
			print(M+N/2.,N/2.*nchunks(M,N),N,'&',M,'&',val,'&',nchunks(M,N), '\\\\')
			# print(val-nchunks(M,N))

