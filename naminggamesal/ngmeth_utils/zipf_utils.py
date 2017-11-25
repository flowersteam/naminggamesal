import copy
import random

from scipy.optimize import curve_fit
from scipy.special import zetac


def zipf_rank_freq(x, a):
	return 1./((x**a)*(1.+zetac(a)))

def fit_zipf(distrib):
	distrib = copy.deepcopy(distrib)
	distrib_2.sort(reverse=True)
	exponent,zipferror = curve_fit(zipf_rank_freq, xdata=range(1,len(distrib_2)+1), ydata=distrib_2)
	return exponent[0],zipferror[0]

def zipfpick(agent=None,pop=None):
	if agent is not None and pop is not None:
		raise ValueError('agent and pop args should not be used at the same time')
	elif agent is not None:
		ms = agent.pick_m()
		return ms,agent.pick_w(m=ms)
	elif pop is not None:
		nbiter = pop._agentlist[0]._vocabulary.get_W()*100
		ag = random.choice(pop._agentlist)
		ms = ag.pick_m()
		return ms,ag.pick_w(m=ms)
	else:
		raise ValueError('pop or agent args should be defined')

def zipf_current(agent=None,pop=None,option='w'):
	if agent is not None and pop is not None:
		raise ValueError('agent and pop args should not be used at the same time')
	elif agent is not None:
		nbiter = agent._vocabulary.get_W()*100
	elif pop is not None:
		nbiter = pop._agentlist[0]._vocabulary.get_W()*100
	else:
		raise ValueError('pop or agent args should be defined')
	distrib = {'m':{},'w':{}}
	delta = 1./nbiter
	for i in nbiter:
		ms,w = zipfpick(agent=agent,pop=pop)
		if ms not in list(distrib['m'].keys()):
			distrib['m'][ms] = delta
		else:
			distrib['m'][ms] += delta
		if w not in list(distrib['w'].keys()):
			distrib['w'][w] = delta
		else:
			distrib['w'][w] += delta
	distrib_m = list(distrib['m'].values())
	distrib_w = list(distrib['w'].values())
	if option == 'm':
		return fit_zipf(distrib_m)
	elif option == 'w':
		return fit_zipf(distrib_w)

def zipf_past(agent=None,pop=None,option='w'):
	if agent is not None and pop is not None:
		raise ValueError('agent and pop args should not be used at the same time')
	elif agent is not None:
		#iterlist = agent._memory
		raise NotImplementedError
	elif pop is not None:
		templist = pop._past
		iterlist = [(p[0],p[1]) for p in templist]
	else:
		raise ValueError('pop or agent args should be defined')
	distrib = {'m':{},'w':{}}
	delta = 1./nbiter
	for elt in iterlist:
		ms,w = elt[0],elt[1]
		if ms not in list(distrib['m'].keys()):
			distrib['m'][ms] = delta
		else:
			distrib['m'][ms] += delta
		if w not in list(distrib['w'].keys()):
			distrib['w'][w] = delta
		else:
			distrib['w'][w] += delta
	distrib_m = list(distrib['m'].values())
	distrib_w = list(distrib['w'].values())
	if option == 'm':
		return fit_zipf(distrib_m)
	elif option == 'w':
		return fit_zipf(distrib_w)

#zipf_current(agent=agent,option='m')[0]
#zipf_current(agent=agent,option='m')[1]
#zipf_current(agent=agent,option='w')[0]
#zipf_current(agent=agent,option='w')[1]
#zipf_current(pop=pop,option='m')[0]
#zipf_current(pop=pop,option='m')[1]
#zipf_current(pop=pop,option='w')[0]
#zipf_current(pop=pop,option='w')[1]