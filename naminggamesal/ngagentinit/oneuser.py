from .agent_init import AgentInit
import copy
import collections

def update_nested_dict(orig_dict, new_dict):
    for key, val in new_dict.items():
        if isinstance(val, collections.Mapping):
            tmp = update_nested_dict(orig_dict.get(key, { }), val)
            orig_dict[key] = tmp
        elif isinstance(val, list):
            orig_dict[key] = (orig_dict.get(key, []) + val)
        else:
            orig_dict[key] = new_dict[key]
    return orig_dict

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
			update_nested_dict(out_cfg,self.new_cfg)
			self.done = True
		return out_cfg


