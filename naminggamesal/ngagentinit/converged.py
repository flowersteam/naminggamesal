from .agent_init import AgentInit
import copy

class Converged(AgentInit):

	def __init__(self,fill_past_inter_mem=True,*args,**kwargs):
		AgentInit.__init__(self,*args,**kwargs)
		self.fill_past_inter_mem = fill_past_inter_mem

	def modified_agent(self,agent, pop, pop_init=False):
		AgentInit.modified_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		if not hasattr(self,'converged_voc'):
			agent._vocabulary.complete_empty()
			self.converged_voc = copy.deepcopy(agent._vocabulary)
		elif pop_init:
			agent._vocabulary = copy.deepcopy(self.converged_voc)
			if self.fill_past_inter_mem:
				if 'past_interactions_sliding_window_local' in agent._memory.keys():
					mp = agent._memory.get_mp('interaction_counts_sliding_window_local')
					mp.fill(voc=self.converged_voc,mem=agent._memory)
				if 'bandit' in agent._memory.keys():
					try:
						mp = agent._memory.get_mp('bandit_laps')
					except:
						mp = agent._memory.get_mp('bandit_negentropy')
					mp.fill(voc=self.converged_voc,mem=agent._memory)

class ConvergedHalfLine(Converged):

	def modified_agent(self,agent, pop, pop_init=False):
		Converged.modified_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		N = pop.nbagent_init/2.
		if len(pop._agentlist) <= N:
			m = agent._vocabulary.get_known_meanings()[0]
			w = agent._vocabulary.get_known_words(m=m)[0]
			if not hasattr(self,'w'):
				self.w = agent._vocabulary.get_new_unknown_w()
			agent._vocabulary.rm(m=m,w=w)
			agent._vocabulary.add(m=m,w=self.w)

