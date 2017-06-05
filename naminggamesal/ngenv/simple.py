from . import Environment
import random

class SimpleEnv(Environment):

	def __init__(self,M, W=None,*args,**kwargs):
		Environment.__init__(self,*args,**kwargs)
		if W is None:
			W = M
		self.M = M
		self.W = W


	def get_M(self):
		return self.M

	def get_W(self):
		return self.W

	def init_agent(self,agent):
		agent._vocabulary.discover_meanings(m_list=range(self.M))
		agent._vocabulary.discover_words(w_list=range(self.W))

