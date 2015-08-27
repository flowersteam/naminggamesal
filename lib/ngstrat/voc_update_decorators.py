#!/usr/bin/python
from . import BaseStrategy

class DecoratorStrategy(BaseStrategy):
	def __init__(self, strategy):
		super(DecoratorStrategy,self).__init__()
		self._strategy = strategy

	def __getattr__(self, name):
		forbidden = ['__init__', '_strategy', '__getattr__', 'update_hearer', 'update_speaker']
		if name in forbidden:
			return super(DecoratorStrategy, self).__getattr__(name)
		else:
			return getattr(self._strategy, name)


class Adaptive(DecoratorStrategy):
	def __init__(self, strategy):
		super(Adaptive,self).__init__(strategy)

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
		if ms==mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)

	def update_speaker(self,ms,w,mh,voc,mem):
		voc.add(ms,w,1)
		if ms==mh:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
