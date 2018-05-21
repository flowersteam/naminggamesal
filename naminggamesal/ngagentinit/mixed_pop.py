from .agent_init import AgentInit
import copy
import random
import collections

def update_nested_dict(orig_dict, new_dict):
    for key, val in new_dict.iteritems():
        if isinstance(val, collections.Mapping):
            tmp = update_nested_dict(orig_dict.get(key, { }), val)
            orig_dict[key] = tmp
        elif isinstance(val, list):
            orig_dict[key] = (orig_dict.get(key, []) + val)
        else:
            orig_dict[key] = new_dict[key]
    return orig_dict

class MixedPop(AgentInit):

	def __init__(self,quantity,new_cfg):
		AgentInit.__init__(self)
		self.new_cfg = copy.deepcopy(new_cfg)
		self.quantity = quantity

	def modify_cfg(self, pop_init=False, **ag_cfg):
		AgentInit.modify_cfg(self,pop_init=pop_init, **ag_cfg)
		out_cfg = copy.deepcopy(ag_cfg)
		if self.condition():
			out_cfg = copy.deepcopy(ag_cfg)
			update_nested_dict(out_cfg,self.new_cfg)
		return out_cfg

	def condition(self):
		self.quantity -= 1
		return self.quantity >= 0


class MixedPopProba(MixedPop):

	def __init__(self,proba,new_cfg):
		AgentInit.__init__(self)
		self.new_cfg = copy.deepcopy(new_cfg)
		self.proba = proba

	def condition(self):
		return random.random() < self.proba
