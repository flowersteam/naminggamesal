from .agent_init import AgentInit
import copy

class Converged(AgentInit):

	def modify_agent(self,agent, pop, pop_init=False):
		AgentInit.modify_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		if not hasattr(self,'converged_voc'):
			agent._vocabulary.complete_empty()
			self.converged_voc = copy.deepcopy(agent._vocabulary)
		elif pop_init:
			agent._vocabulary = copy.deepcopy(self.converged_voc)

class ConvergedHalfLine(Converged):

	def modify_agent(self,agent, pop, pop_init=False):
		Converged.modify_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		N = pop.nbagent_init/2.
		if len(pop._agentlist) <= N:
			m = agent._vocabulary.get_known_meanings()[0]
			w = agent._vocabulary.get_known_words(m=m)[0]
			if not hasattr(self,'w'):
				self.w = agent._vocabulary.get_new_unknown_w()
			agent._vocabulary.rm(m=m,w=w)
			agent._vocabulary.add(m=m,w=self.w)

