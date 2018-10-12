import copy
from . import get_agent_init

class AgentInit(object):

	def __init__(self,sub_agent_init_cfg=None):
		if sub_agent_init_cfg is not None:
			self.sub_agent_init = get_agent_init(**sub_agent_init_cfg)

	def modify_cfg(self, pop_init=False, **ag_cfg):
		ag_cfg = self.modified_cfg(pop_init=pop_init,**ag_cfg)
		if hasattr(self,'sub_agent_init'):
			ag_cfg = self.sub_agent_init.modified_cfg(pop_init=pop_init,**ag_cfg)
		return ag_cfg

	def modify_agent(self,agent, pop, pop_init=False):
		self.modified_agent(pop_init=pop_init,agent=agent,pop=pop)
		if hasattr(self,'sub_agent_init'):
			self.sub_agent_init.modified_agent(pop_init=pop_init,agent=agent,pop=pop)
		if hasattr(pop.env,'init_agent'):
			pop.env.init_agent(agent)

	def modified_cfg(self, pop_init=False, **ag_cfg):
		return copy.deepcopy(ag_cfg)

	def modified_agent(self,agent,pop, pop_init=False):
		pass
