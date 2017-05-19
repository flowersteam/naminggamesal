from .agent_init import AgentInit
import copy

class Converged(AgentInit):

	def modify_agent(self,agent, pop_init=False):
		if not hasattr(self,'converged_voc'):
			agent._vocabulary.complete_empty()
			self.converged_voc = copy.deepcopy(agent._vocabulary)
		elif pop_init:
			agent._vocabulary = copy.deepcopy(self.converged_voc)
