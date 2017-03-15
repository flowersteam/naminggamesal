from . import VocUpdate, get_voc_update
import random
from ... import ngmeth


class AcceptancePolicy(VocUpdate):

	def __init__(self,subvu_cfg):
		VocUpdate.__init__(self)
		self.subvu = get_voc_update(**subvu_cfg)

	def test(ms,w,mh,voc,mem,bool_succ,role, context=[]):
		return True

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if self.test(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, role='hearer', context=context):
			self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, context=context)

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if self.test(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, role='speaker',context=context):
			self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ,context=context)


class AcceptanceBeta(AcceptancePolicy):

	def __init__(self,beta=1.,**cfg2):
		self.beta = beta
		AcceptancePolicy.__init__(self,**cfg2)

	def test(self,*args,**kwargs):
		r = random.random()
		return ( r < self.beta )


class AcceptanceBetaDecrease(AcceptanceBeta):

	def __init__(self,beta=1.,time_scale=100,beta_min=0.1,**cfg2):
		self.beta_min = beta_min
		self.time_scale = time_scale
		AcceptancePolicy.__init__(self,beta,**cfg2)

	def update_hearer(self,*args,**kwargs):
		AcceptanceBeta.update_hearer(self,*args,**kwargs)
		self.decrease()

	def update_speaker(self,*args,**kwargs):
		AcceptanceBeta.update_hearer(self,*args,**kwargs)
		self.decrease()

	def decrease(self):
		self.beta = max(self.beta_min,self.beta - 1./time_scale)


class AcceptanceEntropy(AcceptancePolicy):

	def __init__(self,mem_type='successcount_permw',entropy_func='new_entropy',**cfg2):
		AcceptancePolicy.__init__(self,**cfg2)
		self.memory_policies.append({'mem_type':mem_type})
		self.entropy_func = entropy_func

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		entropy_func = getattr(ngmeth,self.entropy_func)
		S = entropy_func(mem=mem)
		mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		S_new = entropy_func(mem=mem_new)
		return (S_new - S) <= 0


class AcceptanceEntropyBeta(AcceptanceEntropy):

	def __init__(self,beta,**cfg2):
		AcceptanceEntropy.__init__(self,**cfg2)
		self.beta = beta

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		entropy_func = getattr(ngmeth,self.entropy_func)
		S = entropy_func(mem=mem)
		mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		S_new = entropy_func(mem=mem_new)
		deltaS = (S_new - S) 
		r = random.random()
		return r < np.exp(-self.beta*deltaS)