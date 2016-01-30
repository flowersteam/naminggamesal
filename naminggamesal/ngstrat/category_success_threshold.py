
from .naive import StratNaiveCategory,StratNaiveCategoryPlosOne
from . import BaseStrategy
import random
import numpy as np
from intervaltree import IntervalTree, Interval
from scipy.optimize import minimize_scalar


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
		return {'success_matrix':np.zeros((self.nb_boxes,self.nb_boxes,2))}

	def get_coords(self,context):
		m_1 = min(context)
		m_2 = max(context)
		x = int(self.nb_boxes*m_1)
		y = int(self.nb_boxes*m_2)
		return x,y

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
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
		for d,c,bool_succ in sorted(mem['past_interactions'],key=lambda x: -x[0]):
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
		return {'past_interactions':[]}

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		past_int = mem['past_interactions']
		d = abs(context[0]-context[1])
		c = (context[0]+context[1])/2.
		mem['past_interactions'] = past_int[-self.past_window:]+[(d, c, bool_succ)]



class DistSuccessGoal(CategoryDistanceSTStrat):

	def __init__(self, vu_cfg, success_cfg, threshold=0.9, nb_ctxt=20, past_window=100, d_ref=0.1,**strat_cfg2):
		BaseStrategy.__init__(self, vu_cfg=vu_cfg, success_cfg=success_cfg, **strat_cfg2)
		self.threshold = threshold
		self.past_window = past_window
		self.nb_ctxt = nb_ctxt
		self.d_ref = d_ref

	def weight(self,v1,v2):
		return np.exp(-abs(v1-v2)/float(self.d_ref))

	def pick_context(self, voc, mem, context_gen):
		ct_l = [context_gen.next() for i in range(self.nb_ctxt)]
		s_rate = [self.success_rate(context=ct,past_inter=mem['past_interactions']) for ct in ct_l]
		vals = [abs(sr-self.threshold) for sr in s_rate]
		val = min(vals)
		return random.choice([ct_l[i] for i in range(len(ct_l)) if vals[i] == val])

	def get_dist_threshold(self,voc,mem):
		if not mem['past_interactions']:
			return 1.
		else:
			f = lambda x: abs(self.threshold - self.success_rate(x,mem['past_interactions']))
			res = minimize_scalar(f, bounds=(0,1), method='bounded')
			return res.x

	def success_rate(self,dist=None,past_inter=[],context=None):
		if dist is None:
			dist =  abs(context[0] - context[1])
		norm = 0
		val = 0
		for d,c,bool_succ in past_inter:
			w = self.weight(d,dist)
			norm += w
			if bool_succ:
				val += w
		if not norm:
			return 0.
		else:
			return val/norm



class CenterSuccessGoal(DistSuccessGoal):

	def success_rate(self,center=None,past_inter=[],context=None):
		if center is None:
			center =  (context[0] + context[1])/2.
		norm = 0
		val = 0
		for d,c,bool_succ in past_inter:
			w = self.weight(c,center)
			norm += w
			if bool_succ:
				val += w
		if not norm:
			return 0.
		else:
			return val/norm


class DCSuccessGoal(DistSuccessGoal):


	def success_rate(self,past_inter=[],context=None):
		center =  (context[0] + context[1])/2.
		dist =  abs(context[0] - context[1])
		norm = 0
		val = 0
		for d,c,bool_succ in past_inter:
			wc = self.weight(c,center)
			wd = self.weight(d,dist)
			w = wc*wd
			norm += w
			if bool_succ:
				val += w
		if not norm:
			return 0.
		else:
			return val/norm




class DistSuccessSlope(DistSuccessGoal):

	def __init__(self, vu_cfg, success_cfg, dt=10, nb_ctxt=20, past_window=100, d_ref=0.1,**strat_cfg2):
		BaseStrategy.__init__(self, vu_cfg=vu_cfg, success_cfg=success_cfg, **strat_cfg2)
		self.dt = dt
		self.past_window = past_window
		self.nb_ctxt = nb_ctxt
		self.d_ref = d_ref

	def pick_context(self, voc, mem, context_gen):
		ct_l = [context_gen.next() for i in range(self.nb_ctxt)]
		vals = [self.success_slope(context=ct,past_inter=mem['past_interactions']) for ct in ct_l]
		val = max(vals)
		return random.choice([ct_l[i] for i in range(len(ct_l)) if vals[i] == val])


	def success_slope(self,past_inter=[],context=None):
		dt = min(len(past_inter)/3,self.dt)
		T = len(past_inter)-dt
		if not dt:
			return 0
		else:
			past_inter_1 = past_inter[:-dt]
			past_inter_2 = past_inter[-T:]
			old = self.success_rate(context=context,past_inter=past_inter_1)
			new = self.success_rate(context=context,past_inter=past_inter_2)
			return (new-old)/float(dt)


class CenterSuccessSlope(DistSuccessSlope):

	def success_rate(self,center=None,past_inter=[],context=None):
		return CenterSuccessGoal.success_rate(self,center=center,past_inter=past_inter,context=context)


class DCSuccessSlope(DistSuccessSlope):

	def success_rate(self,center=None,past_inter=[],context=None):
		return DCSuccessGoal.success_rate(self,center=center,past_inter=past_inter,context=context)

