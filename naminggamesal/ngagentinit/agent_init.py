import copy

class AgentInit(object):

	def __init__(self):
		pass

	def modify_cfg(self, pop_init=False, **ag_cfg):
		return copy.deepcopy(ag_cfg)

	def modify_agent(self,agent, pop, pop_init=False):
		pop.env.init_agent(agent)
