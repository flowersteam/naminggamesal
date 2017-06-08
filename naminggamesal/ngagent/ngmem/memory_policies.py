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

	def __init__(self,mem_type,time_scale=100,epsilon=0.):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(-1./self.time_scale)
		self.epsilon = epsilon
		self.valmax = 1


	def init_memory(self,mem,voc):
		if hasattr(voc,'_content'):
			assert not hasattr(mem,'interact_count_m')
			assert not hasattr(mem,'interact_count_w')
			mem['interact_count_m'] = np.zeros((voc._M,voc._W))
			mem['interact_count_w'] = np.zeros((voc._M,voc._W))
		else:
			assert not hasattr(mem,'interact_count_voc')
			mem['interact_count_voc'] = voc.__class__(start='empty')

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if hasattr(voc,'_content'):
			for a in [mem["interact_count_m"][ms,:],mem["interact_count_w"][:,w]]:
				a *= self.factor
				a[:] = np.where(a>self.epsilon,a,0.)
				if hasattr(a,'eliminate_zeros'):
					a.eliminate_zeros()
			if self.factor > 0:
				mem['interact_count_w'][ms,w] += 1.-self.factor
				mem['interact_count_m'][ms,w] += 1.-self.factor
		else:
			if ms in mem['interact_count_voc'].get_known_meanings():
				for w1 in mem['interact_count_voc']._content_m[ms].keys():
					mem['interact_count_voc']._content_m[ms][w1] *= self.factor
					if mem['interact_count_voc']._content_m[ms][w1] == 0:
						mem['interact_count_voc'].rm(ms,w1,content_type='m')
			if w in mem['interact_count_voc'].get_known_words():
				for m1 in mem['interact_count_voc']._content_w[w].keys():
					mem['interact_count_voc']._content_w[w][m1] *= self.factor
					if mem['interact_count_voc']._content_w[w][m1] == 0:
						mem['interact_count_voc'].rm(m1,w,content_type='w')
			mem['interact_count_voc'].add(ms,w,val=1.-self.factor,content_type='both')


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

	def init_memory(self,mem,voc):
		InteractionCounts.init_memory(self,mem,voc)
		assert not hasattr(mem,'past_interactions_sliding_window')
		mem['past_interactions_sliding_window'] = []

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if self.time_scale > 0:
			mem['past_interactions_sliding_window'].append((ms,w,1./self.time_scale))
			if hasattr(voc,'_content'):
				mem['interact_count_w'][ms,w] += 1./self.time_scale
				mem['interact_count_m'][ms,w] += 1./self.time_scale
			else:
				mem['interact_count_voc'].add_value(ms,w,1./self.time_scale,content_type='both')

		while len(mem['past_interactions_sliding_window'])>self.time_scale:
			m0,w0,val = mem['past_interactions_sliding_window'].pop(0)
			if hasattr(voc,'_content'):
				mem['interact_count_w'][m0,w0] = max(mem['interact_count_w'][m0,w0] - val , 0)
				mem['interact_count_m'][m0,w0] = max(mem['interact_count_m'][m0,w0] - val , 0)
			else:
				mem['interact_count_voc'].add_value(m0,w0,-val,content_type='both')

	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale


class InteractionCountsSlidingWindowLocal(InteractionCountsSlidingWindow):

	def init_memory(self,mem,voc):
		InteractionCounts.init_memory(self,mem,voc)
		assert not hasattr(mem,'past_interactions_sliding_window_local')
		mem['past_interactions_sliding_window_local'] = {'m':{},'w':{}}

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if self.time_scale > 0:
			if not ms in mem['past_interactions_sliding_window_local']['m'].keys():
				mem['past_interactions_sliding_window_local']['m'][ms] = []
			if not w in mem['past_interactions_sliding_window_local']['w'].keys():
				mem['past_interactions_sliding_window_local']['w'][w] = []
			mem['past_interactions_sliding_window_local']['m'][ms].append((w,1./self.time_scale))
			mem['past_interactions_sliding_window_local']['w'][w].append((ms,1./self.time_scale))
			if hasattr(voc,'_content'):
				mem['interact_count_w'][ms,w] += 1./self.time_scale
				mem['interact_count_m'][ms,w] += 1./self.time_scale
			else:
				mem['interact_count_voc'].add_value(ms,w,1./self.time_scale,content_type='both')

		while ms in mem['past_interactions_sliding_window_local']['m'].keys() and len(mem['past_interactions_sliding_window_local']['m'][ms])>self.time_scale:
			w0,valm = mem['past_interactions_sliding_window_local']['m'][ms].pop(0)
			if hasattr(voc,'_content'):
				mem['interact_count_m'][ms,w0] = max(mem['interact_count_m'][ms,w0] - valm , 0)
			else:
				mem['interact_count_voc'].add_value(ms,w0,-valm,content_type='m')

		while w in mem['past_interactions_sliding_window_local']['w'].keys() and len(mem['past_interactions_sliding_window_local']['w'][w])>self.time_scale:
			m0,valw = mem['past_interactions_sliding_window_local']['w'][w].pop(0)
			if hasattr(voc,'_content'):
				mem['interact_count_w'][m0,w] = max(mem['interact_count_w'][m0,w] - valw , 0)
			else:
				mem['interact_count_voc'].add_value(m0,w,-valw,content_type='w')

		if self.time_scale == 0:
			del mem['past_interactions_sliding_window_local']['m'][ms]
			del mem['past_interactions_sliding_window_local']['w'][w]


	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale

