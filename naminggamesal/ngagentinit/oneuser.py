from .agent_init import AgentInit
import copy

class OneUser(AgentInit):

	def __init__(self):
		AgentInit.__init__(self)
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


class OneDifferent(OneUser):

	def __init__(self,first_ag_cfg):
		OneUser.__init__(self)
		self.first_ag_cfg = first_ag_cfg


	def modify_cfg(self, pop_init=False, **ag_cfg):
		AgentInit.modify_cfg(self,pop_init=pop_init, **ag_cfg)
		out_cfg = copy.deepcopy(ag_cfg)
		if not self.done:
			out_cfg.update(self.first_ag_cfg)
			self.done = True
		return out_cfg


