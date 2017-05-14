import copy

class AgentInit(object):

	def __init__(self):
		pass

	def modify_cfg(self, **ag_cfg):
		return copy.deepcopy(ag_cfg)

	def modify_agent(self,agent):
		pass
