#!/usr/bin/python
from . import BaseStrategy

class DecoratorStrategy(object):
	def __init__(self, strategy):
		self._strategy = strategy
		self.attributes = self.__dict__.keys() + ['__dict__'+'attributes', '__init__', '_strategy', '__getattr__', 'update_hearer', 'update_speaker']

	def __getattr__(self, name):
		if name not in self.attributes:
			ans = object.__getattribute__(self._strategy, name)
		else:
			ans = object.__getattribute__(self, name)
		return ans
		#forbidden = ['__init__', '_strategy', '__getattr__', 'update_hearer', 'update_speaker']
		#if name in dir(self) and not name in ['__getattr__', '__getattribute__']:
		#	return object.__getattribute__(self,name)
		#else:


class Imitation(DecoratorStrategy):
	def __init__(self, strategy):
		super(Imitation,self).__init__(strategy)

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)


class Minimal(DecoratorStrategy):
	def __init__(self, strategy):
		super(Minimal,self).__init__(strategy)

	def update_hearer(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms == mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms == mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)

class BasicLateralInhibition(DecoratorStrategy):
	def __init__(self, strategy, s_init=0.5, d_dec=0.2, d_inh=0.2, d_inc=0.1):
		super(BasicLateralInhibition,self).__init__(strategy)
		self.s_init = s_init
		self.d_dec = d_dec
		self.d_inh = d_inh
		self.d_inc = d_inc
		self.attributes = self.attributes + ['inhibit', 'increase', 'decrease']

	def update_hearer(self,ms,w,mh,voc,mem):
		if voc.get_content()[ms, w] == 0:
			voc.add(ms,w,self.s_init)
		elif ms != mh:
			self.decrease(mh, w, voc)
		else:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in range(voc._M) if m1 != ms]:
				self.inhibit(ms, w, voc)
			for w2 in [w3 for w3 in range(voc._W) if w3 != w]:
				self.inhibit(ms, w2, voc)


	def update_speaker(self,ms,w,mh,voc,mem):
		if voc.get_content()[ms, w] == 0:
			voc.add(ms, w, self.s_init)
		elif ms != mh:
			self.decrease(ms, w, voc)
		else:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in range(voc._M) if m1 != mh]:
				self.inhibit(m, w, voc)
			for w2 in [w3 for w3 in range(voc._W) if w3 != w]:
				self.inhibit(ms, w2, voc)


	def inhibit(self,m,w,voc):
		voc.add(m,w,max(voc.get_content()[m,w] - self.d_inh, 0))

	def increase(self,m,w,voc):
		voc.add(m,w,min(voc.get_content()[m,w] + self.d_inc, 1))

	def decrease(self,m,w,voc):
		voc.add(m,w,max(voc.get_content()[m,w] - self.d_dec, 0))


class InterpolatedLateralInhibition(BasicLateralInhibition):

	def inhibit(self,m,w,voc):
		voc.add(m,w,voc.get_content()[m,w] * (1 - self.d_inh))

	def decrease(self,m,w,voc):
		voc.add(m,w,voc.get_content()[m,w] * (1 - self.d_dec))

	def increase(self, m ,w, voc):
		voc.add(m,w,voc.get_content()[m,w] * (1 - self.d_inc) + self.d_inc)


class Frequency(DecoratorStrategy):

	def update_hearer(self,ms,w,mh,voc,mem):
		y = 1./(2 - voc.get_content()[ms, w]) # y = 1 - 1/(f+1)
		voc.add(ms,w,y) # f <- f+1

	def update_speaker(self,ms,w,mh,voc,mem):
		pass

