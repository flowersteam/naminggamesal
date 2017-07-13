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
			m = voc.get_new_unknown_m()
		else:
			m = voc.get_random_known_m(option='min')
		return m

	def pick_w(self,m,voc,mem,context=[]):
		if m in voc.get_known_meanings():
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

class StratNaiveMemBased(StratNaive):

	def guess_m(self,w,voc,mem,context=[]):
		if w in voc.get_known_words():
			m_list = voc.get_known_meanings(w=w,option=None)
			p_list = [ mem['interact_count_voc'].get_value(m=m1,w=w,role='hearer') for m1 in m_list]
			p = np.ndarray(p_list)
			p = p/p.sum()
			m = np.random.choice(m_list,p=p)
		elif voc.get_unknown_meanings():
			m = voc.get_new_unknown_m()
		else:
			m = voc.get_random_known_m(option='min')
		return m

	def pick_w(self,m,voc,mem,context=[]):
		if m in voc.get_known_meanings():
			w_list = voc.get_known_words(m=m,option=None)
			p_list = [ mem['interact_count_voc'].get_value(m=m,w=w1,role='speaker') for w1 in w_list]
			p = np.ndarray(p_list)
			p = p/p.sum()
			w = np.random.choice(w_list,p=p)
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

######## FOR CATEGORY GAME ############
class StratNaiveCategory(BaseStrategy):

	def pick_context(self, voc, mem, context_gen):
		return context_gen.next()

	def guess_m(self, w, voc, mem, context):
		ml = []
		for m in context:
			if w in voc.get_known_words(m):
				ml.append(m)
		if not ml:
			return None
		else:
			return random.choice(ml)

	def pick_w(self, m, voc, mem, context):
		wl = set(voc.get_known_words(m))
		for c in context:
			if c != m:
				wl = wl - set(voc.get_known_words(c))
		if not wl:
			return voc.get_new_unknown_w()
		else:
			return random.choice(list(wl))

	def pick_m(self, voc, mem, context):
		m = random.choice(context)
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
			return random.choice(list(wl))

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
