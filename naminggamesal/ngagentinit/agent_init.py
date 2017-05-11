import copy

class AgentInit(object):

	def __init__(self,agent_init_type):
		pass

	def modify_cfg(self, **ag_cfg):
		return copy.deepcopy(ag_cfg)

	def modify_agent(self,agent):
		pass