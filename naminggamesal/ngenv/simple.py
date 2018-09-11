from . import Environment
import random
import string
import copy
from builtins import range


from ..tools import holedrange

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


class SimpleEnv(Environment):

	def __init__(self,M=None, W=None,m_list=None, w_list=None, weights_cfg={'weights_type_m':'uniform','weights_type_w':'uniform'}, *args,**kwargs):
		Environment.__init__(self,*args,**kwargs)
		if W is None:
			W = M
		self.M = M
		self.W = W
		self.set_mlist(m_list=m_list)
		self.set_wlist(w_list=w_list)
		self.weights_cfg = weights_cfg

		self.set_M_weights()
		self.set_W_weights()


	def set_M_weights(self):
		if self.weights_cfg['weights_type_m'] == 'uniform':
			# for m in self.m_list:
			# 	self.M_weights[m] = 1
			pass
		elif self.weights_cfg['weights_type_m'] == 'zipf':
			self.M_weights = {}
			for i in range(len(self.m_list)):
				self.M_weights[self.m_list[i]] = 1./(i+1)
		else:
			raise NotImplementedError('weight type for meanings not implemented: '+str(self.weights_cfg['weights_type_m']))

	def set_W_weights(self):
		if self.weights_cfg['weights_type_w'] == 'uniform':
			# for w in self.w_list:
			# 	self.W_weights[w] = 1
			pass
		elif self.weights_cfg['weights_type_w'] == 'zipf':
			self.W_weights = {}
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

	def get_weight_mlist(self,mlist):
		if hasattr(self,'M_weights'):
			try:
				return [self.M_weights[m] for m in mlist]
			except KeyError:
				return None #[1. for _ in mlist]
		else:
			return None # [1. for _ in mlist]

	def get_weight_wlist(self,wlist):
		if hasattr(self,'W_weights'):
			try:
				return [self.W_weights[w] for w in wlist]
			except KeyError:
				return None #[1. for _ in wlist]
		else:
			return None #[1. for _ in wlist]

	def get_M(self):
		return self.M

	def get_W(self):
		return self.W

	def init_agent(self,agent):
		m_list = copy.deepcopy(self.m_list)
		w_list = copy.deepcopy(self.w_list)
		agent._vocabulary.discover_meanings(m_list=m_list,weights=self.get_weight_mlist(mlist=self.m_list))
		agent._vocabulary.discover_words(w_list=w_list,weights=self.get_weight_wlist(wlist=self.w_list))
		for mem_key in list(agent._memory.keys()):
			if hasattr(agent._memory[mem_key],'discover_meanings'):
				agent._memory[mem_key].discover_meanings(m_list=m_list,weights=self.get_weight_mlist(mlist=self.m_list))
			if hasattr(agent._memory[mem_key],'discover_words'):
				agent._memory[mem_key].discover_words(w_list=w_list,weights=self.get_weight_wlist(wlist=self.w_list))

	def set_mlist(self,m_list=None):
		if m_list is None:
			self.m_list = holedrange.HoledRange(self.M)
		else:
			self.m_list = list(m_list)
			self.M = len(self.m_list)

	def set_wlist(self,w_list=None):
		if w_list is None:
			self.w_list = holedrange.HoledRange(self.W)
		else:
			self.w_list = list(w_list)
			self.W = len(self.w_list)

class SimpleEnvRealWords(SimpleEnv):

	def set_wlist(self,w_list=None):
		if w_list is None:
			SimpleEnv.set_wlist(self,w_list=[self.word_generator() for i in range(self.W)])
		else:
			SimpleEnv.set_wlist(self,w_list=w_list)

	def word_generator(self):
		w = ''
		for i in range(3):
			w += random.choice(CONSONANTS)
			w += random.choice(VOWELS)
		return w
