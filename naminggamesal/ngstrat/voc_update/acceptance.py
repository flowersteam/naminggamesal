from . import VocUpdate, get_voc_update
import random
from ... import ngmeth
import numpy as np
import copy
import scipy
from ...ngmeth_utils.srtheo_utils import srtheo_voc


class AcceptancePolicy(VocUpdate):

	def __init__(self,subvu_cfg,acceptance_type='normal'):
		VocUpdate.__init__(self)
		self.acceptance_type = acceptance_type
		self.subvu = get_voc_update(**subvu_cfg)

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		return True

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if self.acceptance_type == 'normal':
			if self.test(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, role='hearer', context=context):
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, context=context)
		elif self.acceptance_type == 'success_when_fail':
			if self.test(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, role='hearer', context=context):
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=True, context=context)
			else:
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, context=context)

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if self.acceptance_type == 'normal':
			if self.test(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, role='speaker', context=context):
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, context=context)
		elif self.acceptance_type == 'success_when_fail':
			if self.test(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, role='speaker', context=context):
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=True, context=context)
			else:
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc,mem=mem,bool_succ=bool_succ, context=context)


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
		AcceptanceBeta.update_speaker(self,*args,**kwargs)
		self.decrease()

	def decrease(self):
		self.beta = max(self.beta_min,self.beta - 1./time_scale)


class AcceptanceEntropy(AcceptancePolicy):

	def __init__(self,mem_policy={'mem_type':'successcount_permw'},entropy_func='new_entropy',**cfg2):
		AcceptancePolicy.__init__(self,**cfg2)
		self.memory_policies.append(copy.deepcopy(mem_policy))
		self.entropy_func = entropy_func

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		entropy_func = getattr(ngmeth,self.entropy_func)
		S = entropy_func(mem=mem)
		mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		S_new = entropy_func(mem=mem_new)
		return (S_new - S) <= 0

#class AcceptanceVocRelatedEntropy(AcceptanceEntropy):
#
#	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
#		entropy_func = getattr(ngmeth,self.entropy_func)
#		voc_new = copy.deepcopy(voc)
#		mem_new = copy.deepcopy(mem)
#		if role == 'hearer':
#			self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
#		elif role == 'speaker':
#			self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
#		S = entropy_func(mem=mem,voc=voc)
#		S_new = entropy_func(mem=mem,voc=voc_new)
#		return (S_new - S) <= 0

class AcceptanceTSMax(AcceptancePolicy):

	def __init__(self,mem_policy={'mem_type':'successcount_permw'},role='both',**cfg2):
		AcceptancePolicy.__init__(self,**cfg2)
		self.memory_policies.append(copy.deepcopy(mem_policy))
		self.role = role

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		if not hasattr(voc,'_content_m'):
			raise ValueError('Acceptance policy TSMax not implemented for this type of vocabulary')
		mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		pop_voc = mem_new['success_mw'] + mem_new['fail_mw']
		voc1 = copy.deepcopy(voc._content)
		voc_new = copy.deepcopy(voc)
		if role == 'hearer':
			self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
		elif role == 'speaker':
			self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
		voc2 = voc_new._content
		if self.role != 'local':
			role = self.role
		if hasattr(self,'strict') and self.strict:
			return srtheo_voc(voc1,pop_voc,role=role) < srtheo_voc(voc2,pop_voc,role=role)
		else:
			return srtheo_voc(voc1,pop_voc,role=role) <= srtheo_voc(voc2,pop_voc,role=role)


class AcceptanceTSMaxNew(AcceptancePolicy):

	def __init__(self,mem_policy={'mem_type':'interaction_counts'},role='both', beta=None, use_new_mem=True,strict=False,**cfg2):
		AcceptancePolicy.__init__(self,**cfg2)
		self.use_new_mem = use_new_mem
		self.memory_policies.append(copy.deepcopy(mem_policy))
		self.role = role
		self.beta = beta
		self.strict = strict

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		if hasattr(self,'use_new_mem') and self.use_new_mem:
			mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		else:
			mem_new = mem
		if hasattr(voc,'_content'):
			pop_voc_m = mem_new['interact_count_m']
			pop_voc_w = mem_new['interact_count_w']
			voc1 = copy.deepcopy(voc._content)
			voc_new = copy.deepcopy(voc)
			if role == 'hearer':
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
			elif role == 'speaker':
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
			voc2 = voc_new._content
			if self.role != 'local':
				role = self.role
			if self.beta is not None:
				print('deprecated')
			return srtheo_voc(voc1,voc2_m=pop_voc_m,voc2_w=pop_voc_w,role=role) <= srtheo_voc(voc2,voc2_m=pop_voc_m,voc2_w=pop_voc_w,role=role)
		else:
			pop_voc = mem_new['interact_count_voc']
			if hasattr(voc,'get_alterable_shallow_copy'):
				voc_new = voc.get_alterable_shallow_copy()
			else:
				voc_new = copy.deepcopy(voc)
			if role == 'hearer':
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
			elif role == 'speaker':
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)

			if self.role != 'local':
				role = self.role
			if self.beta is None:
				if hasattr(self,'strict') and self.strict:
					return srtheo_voc(voc,voc2=pop_voc,role=role) < srtheo_voc(voc_new,voc2=pop_voc,role=role)
				else:
					return srtheo_voc(voc,voc2=pop_voc,role=role) <= srtheo_voc(voc_new,voc2=pop_voc,role=role)
			else:
				#v_ref = srtheo_voc(voc,voc2=mem['interact_count_voc'],role=role)
				v_new = srtheo_voc(voc,voc2=pop_voc,role=role)
				v_update = srtheo_voc(voc_new,voc2=pop_voc,role=role)
				p_1 = np.exp(self.beta*v_new)
				p_2 = np.exp(self.beta*v_update)
				r = random.random()
				if hasattr(self,'strict') and self.strict:
					return r > p_1/(p_1+p_2)
				else:
					return r >= p_1/(p_1+p_2)

class AcceptanceTSMaxNewMemBasedChoices(AcceptanceTSMaxNew):


	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		if hasattr(self,'use_new_mem') and self.use_new_mem:
			mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role=role,bool_succ=bool_succ,context=context)
		else:
			mem_new = mem
		if hasattr(voc,'_content'):
			pop_voc_m = mem_new['interact_count_m']
			pop_voc_w = mem_new['interact_count_w']
			voc1 = copy.deepcopy(voc._content)
			voc_new = copy.deepcopy(voc)
			if role == 'hearer':
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
			elif role == 'speaker':
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
			voc2 = voc_new._content
			if voc2 == voc1:
				return True
			if self.role != 'local':
				role = self.role
			if self.beta is not None:
				print('deprecated')
			if hasattr(self,'strict') and self.strict:
				return srtheo_voc_membased(voc1,voc2_m=pop_voc_m,voc2_w=pop_voc_w,role=role) < srtheo_voc_membased(voc2,voc2_m=pop_voc_m,voc2_w=pop_voc_w,role=role)
			else:
				return srtheo_voc_membased(voc1,voc2_m=pop_voc_m,voc2_w=pop_voc_w,role=role) <= srtheo_voc_membased(voc2,voc2_m=pop_voc_m,voc2_w=pop_voc_w,role=role)
		else:
			pop_voc = mem_new['interact_count_voc']
			if hasattr(voc,'get_alterable_shallow_copy'):
				voc_new = voc.get_alterable_shallow_copy()
			else:
				voc_new = copy.deepcopy(voc)
			if voc_new == voc:
				return True
			if role == 'hearer':
				self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
			elif role == 'speaker':
				self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)

			if self.role != 'local':
				role = self.role
			if self.beta is None:
				return srtheo_voc_membased(voc,voc2=pop_voc,role=role) <= srtheo_voc_membased(voc_new,voc2=pop_voc,role=role)
			else:
				#v_ref = srtheo_voc(voc,voc2=mem['interact_count_voc'],role=role)
				v_old = srtheo_voc_membased(voc,voc2=pop_voc,role=role)
				v_update = srtheo_voc_membased(voc_new,voc2=pop_voc,role=role)
				p_1 = np.exp(self.beta*v_old)
				p_2 = np.exp(self.beta*v_update)
				r = random.random()
				if hasattr(self,'strict') and self.strict:
					return r > p_1/(p_1+p_2)
				else:
					return r >= p_1/(p_1+p_2)



class AcceptanceVocRelatedEntropy(AcceptancePolicy):


	def __init__(self,mem_policy=None):
		VocUpdate.__init__(self)
		if mem_policy is not None:
			self.memory_policies.append(copy.deepcopy(mem_policy))

	def test(self,voc,mem,m,w,axis):
		if axis == 1:
			elt_list = voc.get_known_meanings(w=w)
			if m not in elt_list:
				elt_list.append(m)
			vec1 = np.asarray([mem['success_mw'][m2,w] + mem['fail_mw'][m2,w] for m2 in elt_list])
			vec2 = np.asarray([mem['success_mw'][m2,w] + mem['fail_mw'][m2,w] for m2 in elt_list if m2 != m])
		else:
			elt_list = voc.get_known_words(m=m)
			if w not in elt_list:
				elt_list.append(w)
			vec1 = np.asarray([mem['success_mw'][m,w2] + mem['fail_mw'][m,w2] for w2 in elt_list])
			vec2 = np.asarray([mem['success_mw'][m,w2] + mem['fail_mw'][m,w2] for w2 in elt_list if w2 != w])
		vec1 = vec1/float(sum(vec1))
		vec2 = vec2/float(sum(vec2))
		entr1 = scipy.special.entr(vec1).sum()
		entr2 = scipy.special.entr(vec2).sum()
		return entr2 - entr1

	def add(self,voc,mem,m,w,context):
		if (self.test(voc=voc,mem=mem,m=m,w=w,axis=0) + self.test(voc=voc,mem=mem,m=m,w=w,axis=1)) >= 0:
			voc.add(m,w,context=context)

	def rm_syn(self,voc,mem,m,w):
		w_l = voc.get_known_words(m=m)
		if w in w_l:
			w_l.remove(w)
		for w2 in w_l:
			if self.test(voc=voc,mem=mem,m=m,w=w2,axis=1) < 0:
				voc.rm(m,w2)

	def rm_hom(self,voc,mem,m,w):
		m_l = voc.get_known_meanings(w=w)
		if m in m_l:
			m_l.remove(m)
		for m2 in m_l:
			if self.test(voc=voc,mem=mem,m=m2,w=w,axis=0) < 0:
				voc.rm(m2,w)


	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if bool_succ:
			self.rm_syn(voc=voc,mem=mem,m=ms,w=w)
			self.rm_hom(voc=voc,mem=mem,m=ms,w=w)
		#self.add(voc=voc,mem=mem,m=ms,w=w,context=context)
		voc.add(ms,w,context=context)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if bool_succ:
			self.rm_syn(voc=voc,mem=mem,m=ms,w=w)
			self.rm_hom(voc=voc,mem=mem,m=ms,w=w)
		#self.add(voc=voc,mem=mem,m=ms,w=w,context=context)
		voc.add(ms,w,context=context)
		voc.finish_update()



class AcceptanceEntropyBeta(AcceptanceEntropy):

	def __init__(self,beta=0.1,**cfg2):
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



class AcceptanceVocRelatedEntropyBeta(AcceptanceEntropyBeta):

	def test(self,ms,w,mh,voc,mem,bool_succ,role, context=[]):
		entropy_func = getattr(ngmeth,self.entropy_func)
		if hasattr(voc,'get_alterable_shallow_copy'):
			voc_new = voc.get_alterable_shallow_copy()
		else:
			voc_new = copy.deepcopy(voc)
		mem_new = copy.deepcopy(mem)
		if role == 'hearer':
			self.subvu.update_hearer(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
		elif role == 'speaker':
			self.subvu.update_speaker(ms=ms,w=w,mh=mh,voc=voc_new,mem=mem_new,bool_succ=bool_succ, context=context)
		S = entropy_func(mem=mem,voc=voc)
		S_new = entropy_func(mem=mem,voc=voc_new)
		deltaS = (S_new - S)
		r = random.random()
		return r < np.exp(-self.beta*deltaS)
