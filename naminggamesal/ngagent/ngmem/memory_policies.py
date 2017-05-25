from . import MemoryPolicy
import numpy as np

class SuccessMatrixMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		assert not hasattr(mem,'success_matrix')
		mem['success_matrix'] = np.zeros((self.nb_boxes,self.nb_boxes,2))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		x,y = self.get_coords(context)
		if bool_succ:
			mem['success_matrix'][x,y,0] += 1
		else:
			mem['success_matrix'][x,y,1] += 1


class PastInterMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		assert not hasattr(mem,'past_interactions')
		mem['past_interactions'] = []

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		past_int = mem['past_interactions']
		d = abs(context[0]-context[1])
		c = (context[0]+context[1])/2.
		mem['past_interactions'] = past_int[-self.past_window:]+[(d, c, bool_succ)]



class LastResultMP(MemoryPolicy):

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if bool_succ:
			mem["result"]=1
		else:
			mem["result"]=0

	def init_memory(self,mem,voc):

		assert not hasattr(mem,'result')
		mem["result"]=1

class SuccessCountPerMMP(MemoryPolicy):

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1=ms
		else:
			m1=ms#mh justification: getting information from the other's vocabulary for the hearer
		if bool_succ:
			mem["success_m"][m1]+=1
		else:
			mem["fail_m"][m1]+=1

	def init_memory(self,mem,voc):

		assert not hasattr(mem,'success_m')
		assert not hasattr(mem,'fail_m')
		mem["success_m"] = np.zeros(voc._M)#[0]*voc._M
		mem["fail_m"] = np.zeros(voc._M)#[0]*voc._M

class TimeDecreaseSuccessCountPerMMP(SuccessCountPerMMP):

	def __init__(self,mem_type,time_scale=100):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if self.time_scale == 0:
			self.factor = 0.
		else:
			self.factor = np.exp(-1./self.time_scale)

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1=ms
		else:
			m1=ms#mh justification: getting information from the other's vocabulary for the hearer
		for a in [mem["success_m"][m1],mem["fail_m"][m1]]:
			a *= self.factor
		if bool_succ:
			mem["success_m"][m1]+=1
		else:
			mem["fail_m"][m1]+=1

	def init_memory(self,mem,voc):
		assert not hasattr(mem,'success_m')
		assert not hasattr(mem,'fail_m')
		mem["success_m"] = np.zeros(voc._M)#[0]*voc._M
		mem["fail_m"] = np.zeros(voc._M)#[0]*voc._M



class SuccessCountPerMWMP(MemoryPolicy):
	def init_memory(self,mem,voc):

		assert not hasattr(mem,'success_mw')
		assert not hasattr(mem,'fail_mw')
		mem["success_mw"] = np.zeros((voc._M, voc._W))
		mem["fail_mw"] = np.zeros((voc._M, voc._W))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1 = ms
		else:
			m1 =ms#mh justification: getting information from the other's vocabulary for the hearer
		if bool_succ:
			mem["success_mw"][m1, w]+=1.
		else:
			mem["fail_mw"][m1, w]+=1.

class SuccessCountMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		assert not hasattr(mem,'success')
		assert not hasattr(mem,'fail')
		mem['success'] = 0
		mem['fail'] = 0

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if bool_succ:
			mem['success'] += 1
		else:
			mem['fail'] += 1


class TimeWeightedSuccessCountPerMWMP(SuccessCountPerMWMP):

	def __init__(self,mem_type,time_scale=100):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		self.increment = 1.
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)


	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role == 'speaker':
			m1 = ms
		else:
			m1 = ms#mh justification: getting information from the other's vocabulary for the hearer
		if bool_succ:
			mem["success_mw"][m1, w] += self.increment
		else:
			mem["fail_mw"][m1, w] += self.increment
		self.increment *= self.factor

class TimeDecreaseSuccessCountPerMWMP(TimeWeightedSuccessCountPerMWMP):

	def __init__(self,mem_type,time_scale=100,epsilon=0.01):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)
		self.epsilon = epsilon


	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role == 'speaker':
			m1 = ms
		else:
			m1 = ms#mh justification: getting information from the other's vocabulary for the hearer
		previous_val = mem["success_mw"][m1, w],mem["fail_mw"][m1, w]
		for a in [mem["success_mw"][:,w],mem["fail_mw"][:,w],mem["success_mw"][m1,:],mem["fail_mw"][m1,:]]:
			a *= self.factor
			a[:] = np.where(a>self.epsilon,a,0.)
			if hasattr(a,'eliminate_zeros'):
				a.eliminate_zeros()
		if bool_succ:
			mem["success_mw"][m1, w] = previous_val[0]*self.factor + 1.
		else:
			mem["fail_mw"][m1, w] = previous_val[1]*self.factor + 1.


class InteractionCounts(MemoryPolicy):

	def __init__(self,mem_type,time_scale=100,epsilon=0.01):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)
		self.epsilon = epsilon
		self.valmax = 1


	def init_memory(self,mem,voc):
		assert not hasattr(mem,'interact_count_m')
		assert not hasattr(mem,'interact_count_w')
		mem['interact_count_m'] = np.zeros((voc._M,voc._W))
		mem['interact_count_w'] = np.zeros((voc._M,voc._W))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		for a in [mem["interact_count_m"][ms,:],mem["interact_count_w"][:,w]]:
			a *= self.factor
			a[:] = np.where(a>self.epsilon,a,0.)
			if hasattr(a,'eliminate_zeros'):
				a.eliminate_zeros()
		mem['interact_count_w'][ms,w] += 1.-self.factor
		mem['interact_count_m'][ms,w] += 1.-self.factor

	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)


class InteractionCountsSlidingWindow(InteractionCounts):

	def __init__(self,mem_type,time_scale=100):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		self.valmax = self.time_scale

	def init_memory(self,mem,voc):
		InteractionCounts.init_memory(self,mem,voc)
		assert not hasattr(mem,'past_interactions_sliding_window')
		mem['past_interactions_sliding_window'] = []

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		mem['past_interactions_sliding_window'].append((ms,w))
		mem['interact_count_w'][ms,w] += 1.
		mem['interact_count_m'][ms,w] += 1.
		while len(mem['past_interactions_sliding_window'])>self.time_scale:
			m0,w0 = mem['past_interactions_sliding_window'].pop(0)
			mem['interact_count_w'][m0,w0] -= 1.
			mem['interact_count_m'][m0,w0] -= 1.

	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale
		self.valmax = self.time_scale

