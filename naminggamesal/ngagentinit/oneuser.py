from .agent_init import AgentInit
import copy

class OneUser(AgentInit):

	def __init__(self):
		self.done = False

	def modify_cfg(self, pop_init=False, **ag_cfg):
		AgentInit.modify_cfg(self,pop_init=pop_init, **ag_cfg)
		out_cfg = copy.deepcopy(ag_cfg)
		if not self.done:
			out_cfg['strat_cfg']['strat_type'] = 'user'
			out_cfg['agent_type'] = 'user'
			self.done = True
		return out_cfg

	def modify_agent(self,agent, pop, pop_init=False):
		AgentInit.modify_agent(self,agent=agent,pop=pop,pop_init=pop_init)
		if hasattr(pop.env,'init_agent'):
			pop.env.init_agent(agent)

class OneUserNonInteractive(OneUser):

	def modify_cfg(self, pop_init=False, **ag_cfg):
		AgentInit.modify_cfg(self,pop_init=pop_init, **ag_cfg)
		out_cfg = copy.deepcopy(ag_cfg)
		if not self.done:
			out_cfg['strat_cfg']['strat_type'] = 'user_noninteractive'
			#out_cfg['agent_type'] = 'user'
			self.done = True
		return out_cfg
