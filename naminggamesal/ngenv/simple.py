from . import Environment
import random
import string


VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


class SimpleEnv(Environment):

	def __init__(self,M, W=None, weights_cfg={'weights_type_m':'uniform','weights_type_w':'uniform'}, *args,**kwargs):
		Environment.__init__(self,*args,**kwargs)
		if W is None:
			W = M
		self.M = M
		self.W = W
		self.set_mlist()
		self.set_wlist()
		self.weights_cfg = weights_cfg

		self.set_M_weights()
		self.set_W_weights()


	def set_M_weights(self):
		self.M_weights = {}
		if self.weights_cfg['weights_type_m'] == 'uniform':
			for m in self.m_list:
				self.M_weights[m] = 1
		elif self.weights_cfg['weights_type_m'] == 'zipf':
			for i in range(len(self.m_list)):
				self.M_weights[self.m_list[i]] = 1./(i+1)
		else:
			raise NotImplementedError('weight type for meanings not implemented: '+str(self.weights_cfg['weights_type_m']))

	def set_W_weights(self):
		self.W_weights = {}
		if self.weights_cfg['weights_type_w'] == 'uniform':
			for w in self.w_list:
				self.W_weights[w] = 1
		elif self.weights_cfg['weights_type_w'] == 'zipf':
			if 'zipf_exponent' in list(self.weight_cfg.keys()):
				zipfexp = self.weight_cfg['zipf_exponent']
			else:
				zipfexp = 1.
			for i in range(len(self.w_list)):
				self.W_weights[self.w_list[i]] = 1./(i+1)**zipfexp
		else:
			raise NotImplementedError('weight type for words not implemented: '+str(self.weights_cfg['weights_type_w']))

	def get_weight(self,m=None,w=None):
		if (w is None and m is None ) or (w is not None and m is not None):
			raise ValueError('m and w args should not be set at the same time, or at least one has to be set')
		elif w is not None:
			return self.get_weight_w(w=w)
		elif m is not None:
			return self.get_weight_m(m=m)

	def get_weight_m(self,m):
		if hasattr(self,'M_weights'):
			try:
				return self.M_weights[m]
			except KeyError:
				return 1.
		else:
			return 1.

	def get_weight_w(self,w):
		if hasattr(self,'W_weights'):
			try:
				return self.W_weights[w]
			except KeyError:
				return 1.
		else:
			return 1.

	def get_M(self):
		return self.M

	def get_W(self):
		return self.W

	def init_agent(self,agent):
		agent._vocabulary.discover_meanings(m_list=list(self.m_list),weights=[self.get_weight(m=m) for m in self.m_list])
		agent._vocabulary.discover_words(w_list=list(self.w_list),weights=[self.get_weight(w=w) for w in self.w_list])
		for mem_key in list(agent._memory.keys()):
			if hasattr(agent._memory[mem_key],'discover_meanings'):
				agent._memory[mem_key].discover_meanings(m_list=list(self.m_list),weights=[self.get_weight(m=m) for m in self.m_list])
			if hasattr(agent._memory[mem_key],'discover_words'):
				agent._memory[mem_key].discover_words(w_list=list(self.w_list),weights=[self.get_weight(w=w) for w in self.w_list])

	def set_mlist(self,m_list = None):
		if m_list is None:
			self.m_list = [i for i in range(self.M)]
		else:
			self.m_list = m_list

	def set_wlist(self,w_list):
		if w_list is None:
			self.w_list = [i for i in range(self.W)]
		else:
			self.w_list = w_list

class SimpleEnvRealWords(SimpleEnv):

	def set_wlist(self,w_list=):
		SimpleEnv.set_wlist(self,w_list=[self.word_generator() for i in range(self.W)])

	def word_generator(self):
		w = ''
		for i in range(3):
			w += random.choice(CONSONANTS)
			w += random.choice(VOWELS)
		return w