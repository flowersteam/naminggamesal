from .agent_init import AgentInit

class OwnWordsInit(AgentInit):

	def __init__(self,W_l=None,W_range=None):
		if W_l is None:
			self.W_l = range(W_range)
		else:
			self.W_l = W_l

	def modify_agent(self,agent,pop,pop_init=False):
		AgentInit.modify_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		if self.W_l:
			agent._vocabulary.next_word = self.W_l.pop(0)
