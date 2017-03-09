from . import MemoryPolicy
import numpy as np

class SuccessMatrixMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		mem['success_matrix'] = np.zeros((self.nb_boxes,self.nb_boxes,2))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		x,y = self.get_coords(context)
		if bool_succ:
			mem['success_matrix'][x,y,0] += 1
		else:
			mem['success_matrix'][x,y,1] += 1


class PastInterMP(MemoryPolicy):

	def init_memory(self,mem,voc):
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
		mem["result"]=1

class SuccessCountPerMMP(MemoryPolicy):

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1=ms
		else:
			m1=mh
		if bool_succ:
			mem["success_m"][m1]+=1
		else:
			mem["fail_m"][m1]+=1

	def init_memory(self,mem,voc):
		mem["success_m"] = np.zeros(voc._M)#[0]*voc._M
		mem["fail_m"] = np.zeros(voc._M)#[0]*voc._M



class SuccessCountPerMWMP(MemoryPolicy):
	def init_memory(self,mem,voc):
		mem["success_mw"] = np.zeros((voc._M, voc._W))
		mem["fail_mw"] = np.zeros((voc._M, voc._W))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1 = ms
		else:
			m1 = mh
		if bool_succ:
			mem["success_mw"][m1, w]+=1
		else:
			mem["fail_mw"][m1, w]+=1

class SuccessCountMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		mem['success'] = 0
		mem['fail'] = 0

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if bool_succ:
			mem['success'] += 1
		else:
			mem['fail'] += 1


class TimeWeightedSuccessCountPerMWMP(MemoryPolicy):

	def __init__(self,mem_type,time_scale):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		self.increment = 1.
		self.factor = np.exp(1./t)

	def init_memory(self,mem,voc):
		mem["success_mw"] = np.zeros((voc._M, voc._W))
		mem["fail_mw"] = np.zeros((voc._M, voc._W))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role == 'speaker':
			m1 = ms
		else:
			m1 = mh
		if bool_succ:
			mem["success_mw"][m1, w] += self.increment
		else:
			mem["fail_mw"][m1, w] += self.increment
		self.increment *= self.factor