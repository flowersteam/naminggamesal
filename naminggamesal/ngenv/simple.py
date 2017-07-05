from . import Environment
import random
import string


VOWELS = "aeiou"
CONSONANTS = "".join(set(string.lowercase) - set(VOWELS))


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
		for mem_key in agent._memory.keys():
			if hasattr(agent._memory[mem_key],'discover_meanings'):
				agent._memory[mem_key].discover_meanings(m_list=range(self.M))
			if hasattr(agent._memory[mem_key],'discover_words'):
				agent._memory[mem_key].discover_words(w_list=range(self.W))


class SimpleEnvRealWords(SimpleEnv):


	def __init__(self,*args,**kwargs):
		SimpleEnv.__init__(self,*args,**kwargs)
		self.w_list = [self.word_generator() for i in range(self.W)]

	def word_generator(self):
		w = ''
		for i in range(3):
			w += random.choice(CONSONANTS)
			w += random.choice(VOWELS)
		return w

	def init_agent(self,agent):
		agent._vocabulary.discover_meanings(m_list=range(self.M))
		agent._vocabulary.discover_words(w_list=self.w_list)
		for mem_key in agent._memory.keys():
			if hasattr(agent._memory[mem_key],'discover_meanings'):
				agent._memory[mem_key].discover_meanings(m_list=range(self.M))
			if hasattr(agent._memory[mem_key],'discover_words'):
				agent._memory[mem_key].discover_words(w_list=self.w_list)