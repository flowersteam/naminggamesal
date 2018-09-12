#!/usr/bin/python

from .naive import StratNaive
import random
import numpy as np
import copy

from ..ngmeth_utils.srtheo_utils import srtheo_voc
import copy

class StratTSRMax(StratNaive):

	def __init__(self, vu_cfg, efficient_computing=False, mem_type='interaction_counts_sliding_window_local',global_opt=False,time_scale=10,cache=False,explo_th=False,**strat_cfg2):
		StratNaive.__init__(self,vu_cfg=vu_cfg, **copy.deepcopy(strat_cfg2))
		mp = {'mem_type':mem_type,'time_scale':time_scale}
		if 'interaction_count' not in [ mmpp['mem_type'][:17] for mmpp in self.memory_policies]:
			self.memory_policies.append(mp)
		if cache:
			assert 'proba_of_success_increase' not in [ mmpp['mem_type'][:25] for mmpp in self.memory_policies]
			self.memory_policies.append({'mem_type':'proba_of_success_increase'})
		self.global_opt = global_opt
		self.efficient_computing = efficient_computing
		self.explo_th = explo_th

	def pick_m(self,voc,mem,context):

		m_list = self.get_mval_list(voc=voc,mem=mem,context=context)
		val_max = None

		for key,value in m_list:
			if val_max is None or value > val_max:
				val_max = value
		max_list = []
		for key,value in m_list:
			if value == val_max:
				max_list.append(key)

		m = voc.get_random_m(max_list)

		if 'proba_of_success_increase' in list(mem.keys()):
			m_rm_list = set([m])
			for w2 in voc.get_known_words(m=m):
				m_rm_list = m_rm_list | set(voc.get_known_meanings(w=w2))
			for m2 in m_rm_list:
				if m2 in list(mem['proba_of_success_increase'].keys()):
					del mem['proba_of_success_increase'][m2]
		return m


	def hearer_pick_m(self,voc,mem,context):
		return self.pick_m(voc, mem,context)



	def get_mval_list(self,voc,mem,context):
		m_list = []
		m_explo = None
		test1 = (hasattr(self,'explo_th') and self.explo_th)
		test2 = srtheo_voc(voc,voc2=mem['interact_count_voc']) >= (1.-10**(-5))*float(len(voc.get_known_meanings()))/len(voc.accessible_meanings)
		test3 = len(voc.unknown_meanings)>0
		if test1:
			if test2:
				explo = True
			else:
				explo = False
		else:
			explo = True
		if not test3:
			explo = False
		#print('1:',test1,' 2:',test2,' 3:', test3,' explo:',explo)
		#print('srtheo:',srtheo_voc(voc,voc2=mem['interact_count_voc']))
		if explo:
			m_explo = voc.get_new_unknown_m()
			w_explo = voc.get_new_unknown_w()
			mm_list = voc.get_known_meanings() + [m_explo]
		else:
			mm_list = voc.get_known_meanings()

		global_mat = mem['interact_count_voc']
			#m_explo = None
			#if len(voc.get_unknown_meanings())>0:
			#	m_explo = voc.get_new_unknown_m()
			#	w_explo = voc.get_new_unknown_w()
			#	mm_list = voc.get_known_meanings() + [m_explo]
			#else:
			#	mm_list = voc.get_known_meanings()


		for m1 in mm_list:
			if 'proba_of_success_increase' in list(mem.keys()) and m1 in list(mem['proba_of_success_increase'].keys()):
				val_norm = mem['proba_of_success_increase'][m1]
				m_list.append((m1,val_norm))
			else:
				val = 0
				if m1 == m_explo:
					if len(voc.unknown_words):
						ww_list = voc.unknown_words#[w_explo]
					else:
						ww_list = voc.get_known_words()#[w_explo]
				else:
					ww_list = voc.get_known_words(m=m1)
				for w in ww_list:
					p_success = float(global_mat.get_value(m1,w,content_type='w'))
					p_fail = 1. - p_success
					if hasattr(voc,'get_alterable_shallow_copy'):
						voc_success = voc.get_alterable_shallow_copy()
					else:
						voc_success = copy.deepcopy(voc)
					self.update_speaker(m1, w, m1, voc_success, mem, bool_succ=True, context=context)
					mem_success = mem.simulated_update_memory(ms=m1,w=w,mh=m1,voc=voc_success,role='speaker',bool_succ=True,context=context)
											#global_mat_2 = mem_success['success_mw']+mem_success['fail_mw']

					global_mat_2 = mem_success['interact_count_voc']
											#dS_success = srtheo_voc(voc_success._content,global_mat_2) - srtheo_voc(voc._content,global_mat)
					#if self.efficient_computing:
					#	dS_success = 0
					#	for m_loop in list(set(voc.get_known_meanings(w=w))|set([m1])):
					#		dS_success += 0.5 * (srtheo_voc(voc_success,m=m_loop,voc2=global_mat_2,role='speaker')/(voc_success.get_M()) - srtheo_voc(voc,m=m_loop,voc2=global_mat,role='speaker')/(voc.get_M()))
					#	for w_loop in list(set(voc.get_known_words(m=m1))|set([w])):
					#		dS_success += 0.5 * (srtheo_voc(voc_success,w=w_loop,voc2=global_mat_2,role='hearer') - srtheo_voc(voc,w=w_loop,voc2=global_mat,role='hearer'))
					#else:
					if hasattr(self,'global_opt') and self.global_opt:
						dS_success = srtheo_voc(global_mat_2,voc2=global_mat_2) - srtheo_voc(global_mat,voc2=global_mat)
					else:
						dS_success = srtheo_voc(voc_success,voc2=global_mat_2) - srtheo_voc(voc,voc2=global_mat)
					if hasattr(voc,'get_alterable_shallow_copy'):
						voc_fail = voc.get_alterable_shallow_copy()
					else:
						voc_fail = copy.deepcopy(voc)
					self.update_speaker(m1, w, m1, voc_fail, mem, bool_succ=False, context=context)
					mem_fail = mem.simulated_update_memory(ms=m1,w=w,mh=m1,voc=voc_fail,role='speaker',bool_succ=False,context=context)
								#global_mat_2 = mem_fail['success_mw']+mem_fail['fail_mw']
					global_mat_2 = mem_fail['interact_count_voc']
										#dS_fail = srtheo_voc(voc_fail._content,global_mat_2) - srtheo_voc(voc._content,global_mat)
											#dS_success = srtheo_voc(voc_success._content,global_mat_2) - srtheo_voc(voc._content,global_mat)
					#if self.efficient_computing:
					#	dS_fail = 0
					#	for m_loop in list(set(voc.get_known_meanings(w=w))|set([m1])):
					#		dS_fail += 0.5 * (srtheo_voc(voc_fail,m=m_loop,voc2=global_mat_2,role='speaker')/(voc_fail.get_M()) - srtheo_voc(voc,m=m_loop,voc2=global_mat,role='speaker')/(voc.get_M()))
					#	for w_loop in list(set(voc.get_known_words(m=m1))|set([w])):
					#		dS_fail += 0.5 * (srtheo_voc(voc_fail,w=w_loop,voc2=global_mat_2,role='hearer') - srtheo_voc(voc,w=w_loop,voc2=global_mat,role='hearer'))
					#else:
					if hasattr(self,'global_opt') and self.global_opt:
						dS_fail = srtheo_voc(global_mat_2,voc2=global_mat_2) - srtheo_voc(global_mat,voc2=global_mat)
					else:
						dS_fail = srtheo_voc(voc_fail,voc2=global_mat_2) - srtheo_voc(voc,voc2=global_mat)
					val += p_success * dS_success + p_fail * dS_fail
#				r = random.random()
#				if r < 1./1:
#					if m1 == m_explo:
#						print 'mexplo'
#					print val,p_success,dS_success,dS_fail
#
#					print  srtheo_voc(voc_success,voc2=global_mat_2) , srtheo_voc(voc,voc2=global_mat)
				if m1 == m_explo:
					adj_poss_increase = 1.
					#factor = voc.get_M()/(voc.get_M()+adj_poss_increase)
					#factor = 1.
					if len(voc.unknown_words):
						factor = 1./len(voc.unknown_words)
					else:
						factor = 1./len(voc.accessible_words)
					m_list.append((m_explo,val*factor))
				else:
					m_list.append((m1,val/len(voc.get_known_words(m=m1))))
					if 'proba_of_success_increase' in list(mem.keys()):
						mem['proba_of_success_increase'][m1] = float(val)/len(voc.get_known_words(m=m1))
#			if len(voc.get_unknown_meanings())>0:
#				m_explo = voc.get_new_unknown_m()
	#				w_explo = voc.get_new_unknown_w()
	#				mem_explo = mem.simulated_update_memory(ms=m_explo,w=w_explo,mh=m_explo,voc=voc,role='speaker',bool_succ=False,context=context)
	#
	#				m_list.append((m_explo,mem_val))

		return m_list

class StratTSRMaxMAB(StratTSRMax):

	def __init__(self, vu_cfg, global_opt=False, efficient_computing=False, mem_type='interaction_counts_sliding_window_local',time_scale=10,cache=False,bandit_type='bandit',**strat_cfg2):
		StratTSRMax.__init__(self, vu_cfg=copy.deepcopy(vu_cfg), efficient_computing=efficient_computing, mem_type=mem_type,time_scale=time_scale,cache=cache, **copy.deepcopy(strat_cfg2))
		mp = {'mem_type':bandit_type, 'global_opt':global_opt}
		if 'bandit' not in [ mmpp['mem_type'][:6] for mmpp in self.memory_policies]:
			self.memory_policies.append(mp)

	def get_mval_list(self,voc,mem,context):
		m_list = []
		if len(voc.unknown_meanings)>0:
			m_explo = voc.get_new_unknown_m()
			val_explo = np.random.beta(mem['bandit']['arms']['arm_explo'][0],mem['bandit']['arms']['arm_explo'][1])
			m_list.append((m_explo,val_explo))

		for m in list(mem['bandit']['arms']['others'].keys()):
			val = np.random.beta(mem['bandit']['arms']['others'][m][0],mem['bandit']['arms']['others'][m][1])
			m_list.append((m,val))

		return m_list


class StratTSRMaxHMAB(StratTSRMax):

	def __init__(self, vu_cfg, global_opt=False, efficient_computing=False, mem_type='interaction_counts_sliding_window_local',time_scale=10,cache=False,bandit_type='bandit',**strat_cfg2):
		StratTSRMax.__init__(self, vu_cfg=copy.deepcopy(vu_cfg), efficient_computing=efficient_computing, mem_type=mem_type,time_scale=time_scale,cache=cache, **copy.deepcopy(strat_cfg2))
		mp = {'mem_type':bandit_type,'hierarchical':True,'global_opt':global_opt}
		if 'bandit' not in [ mmpp['mem_type'][:6] for mmpp in self.memory_policies]:
			self.memory_policies.append(mp)

	def get_mval_list(self,voc,mem,context):
		m_list = []
		explore = False
		if len(voc.unknown_meanings)>0:
			explore = True
			m_explo = voc.get_new_unknown_m()
			val_explore = np.random.beta(mem['bandit']['arms']['arm_explo'][0],mem['bandit']['arms']['arm_explo'][1])
			if len(voc.get_known_meanings())>0:
				val_exploit = np.random.beta(mem['bandit']['arms']['arm_exploit'][0],mem['bandit']['arms']['arm_exploit'][1])
				explore = (val_explore > val_exploit)
		if explore:
			m_list.append((m_explo,val_explore))
		else:
			assert len(mem['bandit']['arms']['others'].keys())>0
			for m in list(mem['bandit']['arms']['others'].keys()):
				val = np.random.beta(mem['bandit']['arms']['others'][m][0],mem['bandit']['arms']['others'][m][1])
				m_list.append((m,val))
		return m_list


class LAPSMaxMAB(StratNaive):


	def __init__(self, vu_cfg, global_opt=False, mem_type='interaction_counts_sliding_window_local',time_scale=2,time_scale_bandit=None,gamma=0.01,bandit_type='bandit_laps',**strat_cfg2):
		StratNaive.__init__(self,vu_cfg=vu_cfg, **copy.deepcopy(strat_cfg2))
		mp = {'mem_type':mem_type,'time_scale':time_scale}
		self.mem_type = mem_type
		if 'interaction_count' not in [ mmpp['mem_type'][:17] for mmpp in self.memory_policies]:
			self.memory_policies.append(mp)
		if time_scale_bandit is None:
			mp2 = {'mem_type':bandit_type,'gamma':gamma,'time_scale':time_scale,'global_opt':global_opt}
		else:
			mp2 = {'mem_type':bandit_type,'gamma':gamma,'time_scale':time_scale_bandit,'global_opt':global_opt}
		self.bandit_type = bandit_type
		self.gamma = gamma
		self.time_scale = time_scale
		if 'bandit' not in [ mmpp['mem_type'][:6] for mmpp in self.memory_policies]:
			self.memory_policies.append(mp2)

	def pick_m(self,voc,mem,context):
		if len(voc.get_known_meanings()) == 0 or self.explore_condition(voc=voc,mem=mem,context=context):
			return voc.get_new_unknown_m()
		else:
			laps_val = mem['bandit']['laps_val']
			mp = mem.get_mp(self.bandit_type)
			return mp.pick_arm(mem=mem)

	def hearer_pick_m(self,voc,mem,context):
		return self.pick_m(voc, mem,context)

	def explore_condition(self,voc,mem,context):
		return mem['bandit']['laps_val'] >= (len(voc.get_known_meanings())-1)/len(voc.accessible_meanings)


class LAPSMaxMABExploThreshold(LAPSMaxMAB):

	def __init__(self,vu_cfg,threshold = 1.,epsilon_power=4,*args,**kwargs):
		LAPSMaxMAB.__init__(self,vu_cfg=vu_cfg,*args,**kwargs)
		self.threshold = threshold
		self.epsilon_power = epsilon_power

	def explore_condition(self,voc,mem,context):
		return mem['bandit']['laps_val'] >= self.threshold*(1.-10**(-self.epsilon_power))*(len(voc.get_known_meanings()))/len(voc.accessible_meanings)

