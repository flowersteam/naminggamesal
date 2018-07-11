#!/usr/bin/python

from . import BaseStrategy
import random
import numpy as np
from intervaltree import IntervalTree, Interval

		#####################################NAIVE STRATEGY########################################
class StratNaive(BaseStrategy):

	def guess_m(self,w,voc,mem,context=[]):
		if w in voc.get_known_words():
			m = voc.get_random_known_m(w)
		elif voc.get_unknown_meanings():
			if hasattr(self,'allow_idk') and self.allow_idk:
				m = None
			else:
				m = voc.get_new_unknown_m()
		else:
			if hasattr(self,'allow_idk') and self.allow_idk:
				m = None
			else:
				m = voc.get_random_known_m(option='min')
		return m

	def pick_w(self,m,voc,mem,context=[]):
		if m in voc.get_known_meanings():
			if "prefered words" in list(mem.keys()) and m in list(mem['prefered words'].keys()):
				w = mem['prefered words'][m]
			else:
				w = voc.get_random_known_w(m=m)
		elif voc.get_unknown_words():
			w = voc.get_new_unknown_w()
		else:
			w = voc.get_random_known_w(option='min')
		return w

	def pick_m(self,voc,mem,context=[]):
		m = voc.get_random_m()# randint(0,voc.get_M()-1)
		return m

	def hearer_pick_m(self,voc,mem,context=[]):
		m = self.pick_m(voc,mem,context)
		return m

class StratNaiveExploBiased(StratNaive):

	def pick_m(self,voc,mem,context=[]):
		m_list = voc.get_known_meanings()
		m_explo = voc.get_new_unknown_m()
		if m_explo not in m_list:
			m_list.append(m_explo)
		return random.choice(m_list)

class StratNaiveMemBased(StratNaive):

	def guess_m(self,w,voc,mem,context=[]):
		#if w in voc.get_known_words():
		#	if not voc.get_known_meanings(w=w,option=None):
		#		print('pandas error!!!,!!!')
		if w in voc.get_known_words() and voc.get_known_meanings(w=w,option=None):
			m_list = voc.get_known_meanings(w=w,option=None)
			if 'interact_count_voc' in list(mem.keys()):
				p_list = [ mem['interact_count_voc'].get_value(m=m1,w=w,content_type='w') for m1 in m_list]
				p = np.asarray(p_list)
				if p.sum() == 0:
					m = voc.get_random_m(m_list)
					#print "got only 0s as association values when looking for known meanings of a given word"
					#print p
				else:
					m = np.random.choice(m_list,p=p/p.sum())
			else:
				#try:
				m = voc.get_random_m(m_list)
				#except:
				#	print('pandas error')
				#	if voc.get_unknown_meanings():
				#		m = voc.get_new_unknown_m()
				#	else:
				#		m = voc.get_random_known_m(option='min')
		elif voc.get_unknown_meanings():
			if hasattr(self,'allow_idk') and self.allow_idk:
				m = None
			else:
				m = voc.get_new_unknown_m()
		else:
			if hasattr(self,'allow_idk') and self.allow_idk:
				m = None
			else:
				m = voc.get_random_known_m(option='min')
		return m

	def pick_w(self,m,voc,mem,context=[]):
		#if m in voc.get_known_meanings():
		#	if not voc.get_known_words(m=m,option=None):
		#		print('pandas error!!!')
		if m in voc.get_known_meanings() and voc.get_known_words(m=m,option=None):
			w_list = voc.get_known_words(m=m,option=None)
			if 'interact_count_voc' in list(mem.keys()):
				p_list = [ mem['interact_count_voc'].get_value(m=m,w=w1,content_type='m') for w1 in w_list]
				p = np.asarray(p_list)
				p = p/p.sum()
				if p.sum() != 1:
					w = voc.get_random_w(w_list)
				else:
					w = np.random.choice(w_list,p=p)
			else:
				#try:
				w = voc.get_random_w(w_list)
				#except:
				#	print('pandas error')
				#	if voc.get_unknown_words():
				#		w = voc.get_new_unknown_w()
				#	else:
				#		w = voc.get_random_known_w(option='min')
		elif voc.get_unknown_words():
			w = voc.get_new_unknown_w()
		else:
			w = voc.get_random_known_w(option='min')
		return w

	def pick_m(self,voc,mem,context=[]):
		m = voc.get_random_m()# randint(0,voc.get_M()-1)
		return m

	def hearer_pick_m(self,voc,mem,context=[]):
		m = self.pick_m(voc,mem,context)
		return m

class StratNaiveMemBasedExploBiased(StratNaiveMemBased):

	def pick_m(self,voc,mem,context=[]):
		return StratNaiveExploBiased.pick_m(self,voc=voc,mem=mem,context=context)

######## FOR CATEGORY GAME ############
class StratNaiveCategory(BaseStrategy):

	def pick_context(self, voc, mem, context_gen):
		return next(context_gen)

	def guess_m(self, w, voc, mem, context):
		ml = [m for m in context if w in voc.get_known_words(m)]
		if not ml:
			return None
		else:
			return voc.get_random_m(ml)

	def pick_w(self, m, voc, mem, context):
		wl = set(voc.get_known_words(m))
		for c in context:
			if c != m:
				wl = wl - set(voc.get_known_words(c))
		if not wl:
			return voc.get_new_unknown_w()
		else:
			return voc.get_random_w(list(wl))

	def pick_m(self, voc, mem, context):
		m = voc.get_random_m(m_list=context)
		#voc.minmax_slice(m,context)
		return m

	def hearer_pick_m(self, voc, mem, context):
		m = self.pick_m(voc, mem, context)
		return m

######## FOR CATEGORY GAME, AS IN PAPERS ############
class StratNaiveCategoryPlosOne(StratNaiveCategory):

	def pick_w(self, m, voc, mem, context):
		wl = voc.get_known_words(m,option='max')
		if not wl:
			return voc.get_new_unknown_w()
		else:
			return voc.get_random_w(list(wl))

#	def init_memory(self,voc):
#		return IntervalTree([Interval(0,1,None)])
#
#	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
#		cat = voc.get_category(ms)
#		if bool_succ:
#			iv = Interval(cat.begin,cat.end,w)
#			mem.chop(cat.begin,cat.end)
#			iv_before = Interval(-1,0,[None])
#			iv_after = Interval(1,2,[None])
#			for iv2 in [i for i in sorted(mem) if i.end==iv.begin]:
#				iv_before = iv2
#			for iv2 in [i for i in sorted(mem) if iv.end==i.begin]:
#				iv_after = iv2
#			if iv_before.data != w and iv_after.data != w:
#				mem.add(iv)
#			elif iv_before.data == w and iv_after.data != w:
#				mem.chop(iv_before.begin,iv_before.end)
#				mem.add(Interval(iv_before.begin,cat.end,w))
#			elif iv_before.data != w and iv_after.data == w:
#				mem.chop(iv_after.begin,iv_after.end)
#				mem.add(Interval(cat.begin,iv_after.end,w))
#			elif iv_before.data == w and iv_after.data == w:
#				mem.chop(iv_before.begin,iv_after.end)
#				mem.add(Interval(iv_before.begin,iv_after.end,w))
#		elif not bool_succ and role == 'hearer' and len(cat.data) > 1:#!!!!!!!!!!
#			w1 = cat.data.pop()
#			w2 = cat.data.pop()
#			cat.data.append(w1)
#			cat.data.append(w2)
