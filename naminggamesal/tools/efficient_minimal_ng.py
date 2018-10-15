
import numpy as np
import time
from collections import defaultdict
from memory_profiler import memory_usage

def stop_condition(T,pop,Tmax,monitor_T):
	if T == monitor_T:
		print(memory_usage())
	return (T >= Tmax) or (T>0 and len(pop) == 1)

def pick_agent(pop):
	p = np.asarray(list(pop.values()),dtype=float)
	if len(p) == 1.:
		return list(pop.keys())[0]
	p /= p.sum()
	try:
		ans = np.random.choice(list(pop.keys()),p=p)
	except KeyboardInterrupt:
		raise
	except:
		print(len(pop))
		print(list(pop.keys()))
		print(list(pop.values()))
		return list(pop.keys())[0]
	pop[ans] -= 1
	if pop[ans] == 0:
		del pop[ans]
	return ans

def run(Tmax,N):
	try:
		pop = defaultdict(int)
		pop[()] = N
		max_word = -1
		monitor_T = int(1./np.sqrt(2.)*N**(1.5))
		T = 0
		while not stop_condition(T,pop,Tmax,N):
			sp = pick_agent(pop)
			hr = pick_agent(pop)
			if sp == ():
				max_word += 1
				sp = (max_word,)
				hr = tuple(sorted((*hr,max_word)))
				if pop[()] == 0:
					del pop[()]
				pop[sp] += 1
				pop[hr] += 1
			else:
				w = np.random.choice(sp)
				if w in hr:
					pop[(w,)] += 2
				else:
					hr = tuple(sorted((*hr,max_word)))
					pop[sp] += 1
					pop[hr] += 1
			T += 1
		print('end',memory_usage())
		return T
	except:
		print('T',T)
		print('mem',memory_usage())
		print('len',len(pop))


if __name__ == '__main__':
	start = time.time()
	print(memory_usage())
	N=2000
	print('N',N)
	t = run(Tmax = 10000000, N=N)
	print(t)
	print(time.time()-start,'seconds')