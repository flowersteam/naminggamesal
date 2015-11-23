#!/usr/bin/python

from . import Interaction
import random
import numpy as np
from .. import ngmeth


def proba_info(agent1, agent2, alpha = 1.):        #based on information measure
	if np.count_nonzero(agent1._vocabulary.get_content())*np.count_nonzero(agent2._vocabulary.get_content()) == 0:
		return 1
	tempmat = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
	tempm = np.sum(tempmat)
	return 1.-(ngmeth.tempentropy(agent1._M-tempm, agent2._W-tempm)/ngmeth.tempentropy(agent1._M, agent2._W))

def proba_info_emptyplusshared(agent1, agent2, alpha = 1.):        #based on information measure
	mat_shared = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
	m_shared = np.sum(mat_shared)
	shared = 1.-(ngmeth.tempentropy(agent1._M-m_shared, agent1._W-m_shared)/ngmeth.tempentropy(agent1._M, agent1._W))
	m_empty = agent2._M - np.sum(agent2._vocabulary.get_content())
	empty = 1.-(ngmeth.tempentropy(agent1._M-m_empty, agent1._W-m_empty)/ngmeth.tempentropy(agent1._M, agent1._W))
	return shared + alpha*empty

def proba_info_shared(agent1, agent2, alpha = 1.):        #based on information measure
	mat_shared = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
	m_shared = np.sum(mat_shared)
	shared = 1.-(ngmeth.tempentropy(agent1._M-m_shared, agent1._W-m_shared)/ngmeth.tempentropy(agent1._M, agent1._W))
	m_empty = agent2._M - np.sum(agent2._vocabulary.get_content())
	empty = 1.-(ngmeth.tempentropy(agent1._M-m_empty, agent1._W-m_empty)/ngmeth.tempentropy(agent1._M, agent1._W))
	if empty == 1:
		return alpha
	return shared 

def proba_info_relativeshared(agent1, agent2, alpha = 1.):        #based on information measure
	mat_shared = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
	m_shared = np.sum(mat_shared)
	shared = 1.-(ngmeth.tempentropy(agent1._M-m_shared, agent1._W-m_shared)/ngmeth.tempentropy(agent1._M, agent1._W))
	m_empty = agent2._M - np.sum(agent2._vocabulary.get_content())
	empty = 1.-(ngmeth.tempentropy(agent1._M-m_empty, agent1._W-m_empty)/ngmeth.tempentropy(agent1._M, agent1._W))
	if empty == 1:
		return alpha
	return shared/(1.-alpha*empty)


def FUNC2(agent1, agent2):         #always half
	return 0.5

def FUNC3(agent1, agent2):         #random (equivalent to 0.5?)
	return random.random()


##########
class FabienInteraction(Interaction):

	def __init__(self, proba_func='proba_info', **interact_cfg2):
		super(FabienInteraction,self).__init__(**interact_cfg2)
		self.proba_func = globals()[proba_func]  #Use globals or locals?
		if not hasattr(self,'alpha'):
			self.alpha = 1.


	def interact(self, speaker, hearer, pop):
		r = random.random()
		if self.proba_func(speaker, hearer, self.alpha) > r:
			self.base_interact(speaker, hearer, pop)

	def base_interact(self, speaker, hearer, pop):
		ms = speaker.pick_m()
		w =  speaker.pick_w(ms)
		mh = hearer.guess_m(w)
		bool_succ = hearer.eval_success(ms=ms, w=w, mh=mh)
		speaker.update_speaker(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
		hearer.update_hearer(ms=ms,w=w,mh=mh,bool_succ=bool_succ)
		self._last_info = [ms,w,mh,bool_succ,speaker._id,hearer._id]
