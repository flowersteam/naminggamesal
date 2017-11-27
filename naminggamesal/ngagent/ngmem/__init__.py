from importlib import import_module
import collections
import copy

#####Classe de base
mempolicy_class={
'success_matrix':'memory_policies.SuccessMatrixMP',
'past_interactions':'memory_policies.PastInterMP',
'successcount':'memory_policies.SuccessCountMP',
'successcount_perm':'memory_policies.SuccessCountPerMMP',
'successcount_permw':'memory_policies.SuccessCountPerMWMP',
'timeweighted_successcount_permw':'memory_policies.TimeWeightedSuccessCountPerMWMP',
'timedecrease_successcount_permw':'memory_policies.TimeDecreaseSuccessCountPerMWMP',
'timedecrease_successcount_perm':'memory_policies.TimeDecreaseSuccessCountPerMMP',
'lastresult':'memory_policies.LastResultMP',
'interaction_counts':'memory_policies.InteractionCounts',
'interaction_counts_sliding_window':'memory_policies.InteractionCountsSlidingWindow',
'interaction_counts_sliding_window_local':'memory_policies.InteractionCountsSlidingWindowLocal',
'proba_of_success_increase':'memory_policies.ProbaSuccessIncrease',
'bandit':'memory_policies.BetaMAB',
}

def get_memory(memory_policies,voc=None):
	return Memory(memory_policies=memory_policies,voc=voc)

def get_memory_policy(mem_type,**mem_pol_cfg2):
	tempstr = mem_type
	if tempstr in list(mempolicy_class.keys()):
		tempstr = mempolicy_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	return getattr(_tempmod,tempclass)(mem_type=mem_type,**mem_pol_cfg2)



class Memory(collections.MutableMapping):

	def __init__(self, memory_policies, voc=None):
		self.store = dict()
		self.memory_policies = []
		self.mpclasses = []
		for mp in memory_policies:
			if mp['mem_type'] not in self.mpclasses:
				self.mpclasses.append(mp['mem_type'])
				self.memory_policies.append(get_memory_policy(**mp))
			else:
				print(mp['mem_type'],'already in memory policies, not appending')
		self.init_memory(voc=voc)

	def __getitem__(self, key):
		return self.store[key]

	def __setitem__(self, key, value):
		self.store[key] = value

	def __delitem__(self, key):
		del self.store[key]

	def __iter__(self):
		return iter(self.store)

	def __len__(self):
		return len(self.store)

	def update_memory(self,ms,w,mh,voc,role,bool_succ,context=[]):
		for mem_p in self.memory_policies:
			mem_p.update_memory(mem=self,ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)

	def init_memory(self,voc=None):
		for mem_p in self.memory_policies:
			mem_p.init_memory(mem=self,voc=voc)
		if voc is not None:
			voc.finish_update()

	def simulated_update_memory(self,ms,w,mh,voc,role,bool_succ,context=[],allow_alterableshallow=True):
		if allow_alterableshallow:
			fake_mem = Memory(memory_policies=[])
			fake_mem.mpclasses = copy.deepcopy(self.mpclasses)
			fake_mem.memory_policies = copy.deepcopy(self.memory_policies)
			for k in list(self.store.keys()):
				if hasattr(self.store[k],'get_alterable_shallow_copy'):
					fake_mem[k] = self.store[k].get_alterable_shallow_copy()
				else:
					fake_mem[k] = copy.deepcopy(self.store[k])
		else:
			fake_mem = copy.deepcopy(self)
		fake_mem.update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		return fake_mem



class MemoryPolicy(object):

	def __init__(self,mem_type):
		self.mem_type = mem_type

	def __eq__(self,other):
		return self.mem_type == other.mem_type

	def init_memory(self,mem,voc):
		pass

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		pass
