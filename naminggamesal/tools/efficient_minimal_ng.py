
import numpy as np
import random
import time
from collections import defaultdict
from memory_profiler import memory_usage

def stop_condition(T,pop,Tmax,monitor_T):
	if T == monitor_T:
		print(memory_usage())
	return (T >= Tmax) or (T>0 and len(pop) == 1)

def new_stop_condition(T,pop,Tmax,monitor_T):
	if T == monitor_T:
		print(memory_usage())
	return (T >= Tmax) or (T>0 and len(pop['d1']) == 1)

def pop_add(ag,pop):
	s = pop['d1'][ag]+1
	pop['d1'][ag] = s
	if s > 1:
		pop['d2'][s-1].remove(ag)
		pop['d2bis'][s-1]-=1
		if pop['d2bis'][s-1] == 0:
			del pop['d2bis'][s-1]
			del pop['d2'][s-1]
	pop['d2bis'][s]+=1
	pop['d2'][s].add(ag)
	pop['N'] += 1

def pop_rm(ag,pop):
	s = pop['d1'][ag]-1
	if s > 0:
		pop['d1'][ag] = s

		pop['d2bis'][s] += 1
		pop['d2'][s].add(ag)
	else:
		del pop['d1'][ag]
	pop['d2'][s+1].remove(ag)
	pop['d2bis'][s+1]-=1
	if pop['d2bis'][s+1] == 0:
		del pop['d2bis'][s+1]
		del pop['d2'][s+1]
	pop['N'] -= 1


def pop_init(N):
	pop = {'d1':defaultdict(int),'d2':defaultdict(set),'d2bis':defaultdict(int)}
	pop['d1'][()] = N
	pop['d2'][N].add(())
	pop['d2bis'][N] = 1
	pop['N'] = float(N)
	return pop

def pick_size(pop):
	keys = list(pop['d2bis'].keys())
	# print(keys)
	if len(keys) == 1:
		return keys[0]
	# keys = np.asarray(keys)
	values = [k*pop['d2bis'][k]/pop['N'] for k in keys]
	try:
		s = np.random.choice(keys,p=values)
	except:
		print(values)
		print(pop['d2bis'])
		print(sum(values))
		raise
	# print(values)
	return s

def new_pick_agent(pop):
	s = pick_size(pop=pop)
	# print(s)
	# print(pop['d2'],'blah')
	ag = random.sample(pop['d2'][s],1)[0]
	pop_rm(ag=ag,pop=pop)
	return ag

def new_run(Tmax,N):
	try:
		pop = pop_init(N=N)
		max_word = -1
		monitor_T = int(1./np.sqrt(2.)*N**(1.5))
		T = 0
		while not new_stop_condition(T,pop,Tmax,N):
			sp = new_pick_agent(pop)
			hr = new_pick_agent(pop)
			if sp == ():
				max_word += 1
				sp = (max_word,)
				# hr = tuple(sorted((*hr,max_word)))
				hr = tuple(sorted(hr+(max_word,)))
			else:
				w = np.random.choice(sp)
				if w in hr:
					sp = (w,)
					hr = (w,)
				else:
					# hr = tuple(sorted((*hr,max_word)))
					hr = tuple(sorted(hr+(max_word,)))
			pop_add(pop=pop,ag=sp)
			pop_add(pop=pop,ag=hr)
			T += 1
		print('end',memory_usage())
		return T
	except:
		print('T',T)
		print('mem',memory_usage())
		print('len d1',len(pop['d1']))
		print('len d2',len(pop['d2']))
		raise





#################





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
				# hr = tuple(sorted((*hr,max_word)))
				hr = tuple(sorted(hr+(max_word,)))
				if pop[()] == 0:
					del pop[()]
				pop[sp] += 1
				pop[hr] += 1
			else:
				w = np.random.choice(sp)
				if w in hr:
					pop[(w,)] += 2
				else:
					hr = tuple(sorted(hr+(max_word,)))
					# hr = tuple(sorted((*hr,max_word)))
					pop[sp] += 1
					pop[hr] += 1
			T += 1
		print('end',memory_usage())
		return T
	except:
		print('T',T)
		print('mem',memory_usage())
		print('len',len(pop))
		raise


if __name__ == '__main__':
	start = time.time()
	print(memory_usage())
	N=10000
	print('N',N)
	try:
		t = new_run(Tmax=100000, N=N)
		print(t)
	finally:
		print(time.time()-start,'seconds')
