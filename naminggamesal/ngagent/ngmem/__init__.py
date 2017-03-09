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
'lastresult':'memory_policies.LastResultMP'
}

def get_memory(memory_policies,voc=None):
	return Memory(memory_policies=memory_policies,voc=voc)

def get_memory_policy(mem_type,**mem_pol_cfg2):
	tempstr = mem_type
	if tempstr in mempolicy_class.keys():
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
		for mp in memory_policies:
			self.memory_policies.append(get_memory_policy(**mp))
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

	def update_memory(self,*args,**kwargs):
		for mem_p in self.memory_policies:
			mem_p.update_memory(mem=self,*args,**kwargs)

	def init_memory(self,voc=None):
		for mem_p in self.memory_policies:
			mem_p.init_memory(mem=self,voc=voc)
		if voc is not None:
			voc.finish_update()

	def simulated_update_memory(self,*args,**kwargs):
		fake_mem = copy.deepcopy(self)
		fake_mem.update_memory(*args,**kwargs)
		return fake_mem



class MemoryPolicy(object):

	def __init__(self,mem_type):
		self.mem_type = mem_type

	def init_memory(self,mem,voc):
		pass

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		pass
