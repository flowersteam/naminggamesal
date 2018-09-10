from .agent_init import AgentInit

class OwnWordsInit(AgentInit):

	def __init__(self,W_l=None,W_range=None,M=1):
		if W_l is None:
			self.W_l = W_range
			self.range_mode = True
		else:
			self.W_l = W_l
			self.range_mode = False
		self.M = M

	def modify_agent(self,agent,pop,pop_init=False):
		AgentInit.modify_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		if self.W_l:
			if not hasattr(self,'M') or self.M == 1:
				if self.range_mode:
					agent._vocabulary.next_word = self.W_l-1
					self.W_l -= 1
				else:
					agent._vocabulary.next_word = self.W_l.pop(0)
			else:
				if self.range_mode:
					agent._vocabulary.next_word = range(self.W_l-self.M,self.W_l)
					self.W_l = self.W_l-self.M
				else:
					agent._vocabulary.next_word = self.W_l[:self.M]
					self.W_l = self.W_l[self.M:]
