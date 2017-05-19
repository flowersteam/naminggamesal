from .agent_init import AgentInit
import copy

class Converged(AgentInit):

	def modify_agent(self,agent):
		if not hasattr(self.converged_voc):
			agent._vocabulary.complete_empty()
			self.converged_voc = copy.deepcopy(agent._vocabulary)
		else:
			agent._vocabulary = copy.deepcopy(self.converged_voc)
