
from .naive import StratNaiveCategory,StratNaiveCategoryPlosOne
from . import BaseStrategy
import random
import numpy as np
from intervaltree import IntervalTree, Interval



class CategorySuccessThresholdStrat(StratNaiveCategoryPlosOne): #For the moment only for context size = 2

	def __init__(self, vu_cfg, success_cfg, threshold=0.9, nb_ctxt=20, nb_boxes=10, **strat_cfg2):
		BaseStrategy.__init__(self, vu_cfg=vu_cfg, success_cfg=success_cfg, **strat_cfg2)
		self.threshold = threshold
		self.nb_ctxt = nb_ctxt
		self.nb_boxes = nb_boxes


	def pick_context(self, voc, mem, context_gen):
		ct_l = [context_gen.next() for i in range(self.nb_ctxt)]
		coords = [self.get_coords(ct) for ct in ct_l]
		cf_ab_min = 1
		cf_be_max = 0
		above = []
		below = []
		notknown = []
		for i in range(len(coords)):
			cf = self.eval_confidence(mem,*coords[i])
			if cf > self.threshold:
				above.append((i,cf))
				cf_ab_min = min(cf_ab_min,cf)
			elif cf >= 0 or mem['success_matrix'][coords[i][0],coords[i][1],1]>0:
				below.append((i,cf))
				cf_be_max = max(cf_be_max,cf)
			else:
				notknown.append(i)
		if below:
			return random.choice([ct_l[i] for i,cf in below if cf == cf_be_max])
		elif notknown:
			return ct_l[random.choice(notknown)]
		else:
			return random.choice([ct_l[i] for i,cf in above if cf == cf_ab_min])


	def init_memory(self,voc):
		return {'success_matrix':np.zeros((self.nb_boxes,self.nb_boxes,2)),'success_dict':StratNaiveCategoryPlosOne.init_memory(self,voc)}

	def get_coords(self,context):
		m_1 = min(context)
		m_2 = max(context)
		x = int(self.nb_boxes*m_1)
		y = int(self.nb_boxes*m_2)
		return x,y

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		StratNaiveCategoryPlosOne.update_memory(self,ms,w,mh,voc,mem['success_dict'],role,bool_succ,context)
		x,y = self.get_coords(context)
		if bool_succ:
			mem['success_matrix'][x,y,0] += 1
		else:
			mem['success_matrix'][x,y,1] += 1


	def eval_confidence(self,mem,x,y):
		s = mem['success_matrix'][x,y,0]
		f = mem['success_matrix'][x,y,1]
		if f+s == 0:
			return 0.
		else:
			return s/float(s+f)

	def pick_w(self, m, voc, mem, context):
		return StratNaiveCategoryPlosOne.pick_w(self, m, voc, mem['success_dict'], context)



class CategoryDistCenterStrat(CategorySuccessThresholdStrat): #For the moment only for context size = 2

	def get_coords(self,context):
		m_1 = np.mean(context)
		m_2 = abs(context[0]-context[1])
		x = int(self.nb_boxes*m_1)
		y = int(self.nb_boxes*m_2)
		return x,y


class CategoryDistanceSTStrat(CategorySuccessThresholdStrat):

	def __init__(self, vu_cfg, success_cfg, threshold=0.9, nb_ctxt=20, past_window=100, **strat_cfg2):
		BaseStrategy.__init__(self, vu_cfg=vu_cfg, success_cfg=success_cfg, **strat_cfg2)
		self.threshold = threshold
		self.past_window = past_window
		self.nb_ctxt = nb_ctxt

	def pick_context(self, voc, mem, context_gen):
		ct_l = [context_gen.next() for i in range(self.nb_ctxt)]
		dist = [abs(ct[0]-ct[1]) for ct in ct_l]
		thresh_dist = self.get_dist_threshold(voc,mem)
		above = 1.
		below = 0.
		for i in range(len(dist)):
			if dist[i] >= thresh_dist:
				above = min(above, dist[i])
			else:
				below = max(below,dist[i])
		if below:
			return random.choice([ct_l[i] for i in range(len(dist)) if dist[i] == below])
		else:
			return random.choice([ct_l[i] for i in range(len(dist)) if dist[i] == above])

	def get_dist_threshold(self,voc,mem):
		s = 0
		f = 0
		d_val = 1.
		for d,bool_succ in sorted(mem['past_interactions'],key=lambda x: -x[0]):
			if bool_succ:
				s += 1
			else:
				f += 1
			if s/float(s+f) < self.threshold:
				return d_val
			else:
				d_val = d
		return d_val

	def init_memory(self,voc):
		return {'past_interactions':[],'success_dict':StratNaiveCategoryPlosOne.init_memory(self,voc)}

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		StratNaiveCategoryPlosOne.update_memory(self,ms,w,mh,voc,mem['success_dict'],role,bool_succ,context)
		past_int = mem['past_interactions']
		d = abs(context[0]-context[1])
		mem['past_interactions'] = past_int[-self.past_window:]+[(d, bool_succ)]


