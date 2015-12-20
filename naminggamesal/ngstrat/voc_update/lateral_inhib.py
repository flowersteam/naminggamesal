from . import VocUpdate


class BasicLateralInhibition(VocUpdate):
	def __init__(self, s_init=0.5, d_dec=0.2, d_inh=0.2, d_inc=0.1):
		self.s_init = s_init
		self.d_dec = d_dec
		self.d_inh = d_inh
		self.d_inc = d_inc

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ):
		if voc._content[ms, w] == 0:
			voc.add(ms,w,self.s_init)
		elif not bool_succ:
			self.decrease(mh, w, voc)
		else:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in voc.get_known_meanings(w=w,option=None) if m1 != ms]:
				self.inhibit(ms, w, voc)
			for w2 in [w3 for w3 in voc.get_known_words(m=ms,option=None) if w3 != w]:
				self.inhibit(ms, w2, voc)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ):
		if voc._content[ms, w] == 0:
			voc.add(ms, w, self.s_init)
		elif not bool_succ:
			self.decrease(ms, w, voc)
		else:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in voc.get_known_meanings(w=w,option=None) if m1 != mh]:
				self.inhibit(m, w, voc)
			for w2 in [w3 for w3 in voc.get_known_words(m=ms,option=None) if w3 != w]:
				self.inhibit(ms, w2, voc)
		voc.finish_update()

	def inhibit(self,m,w,voc):
		voc.add(m,w,max(voc._content[m,w] - self.d_inh, 0))

	def increase(self,m,w,voc):
		voc.add(m,w,min(voc._content[m,w] + self.d_inc, 1))

	def decrease(self,m,w,voc):
		voc.add(m,w,max(voc._content[m,w] - self.d_dec, 0))


class InterpolatedLateralInhibition(BasicLateralInhibition):

	def inhibit(self,m,w,voc):
		voc.add(m,w,voc._content[m,w] * (1 - self.d_inh))

	def decrease(self,m,w,voc):
		voc.add(m,w,voc._content[m,w] * (1 - self.d_dec))

	def increase(self, m ,w, voc):
		voc.add(m,w,voc._content[m,w] * (1 - self.d_inc) + self.d_inc)

class BasicLateralInhibitionHearerOnly(BasicLateralInhibition):
	def update_speaker(self,ms,w,mh,voc,mem,bool_succ):
		voc.finish_update()


class BasicLateralInhibitionHearerOnlyFailure(BasicLateralInhibition):

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ):
		if voc._content[ms, w] == 0:
			voc.add(ms, w, self.s_init)
		elif bool_succ:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in voc.get_known_meanings(w=w,option=None) if m1 != mh]:
				self.inhibit(m, w, voc)
			for w2 in [w3 for w3 in voc.get_known_words(m=ms,option=None) if w3 != w]:
				self.inhibit(ms, w2, voc)
		voc.finish_update()


class BLISEpirob(BasicLateralInhibition):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ):
		if not voc.get_known_meanings(w=w,option=None):
			voc.add(ms,w,self.s_init)
		elif not bool_succ:
			self.decrease(mh, w, voc)
			self.increase(ms, w, voc)
		else:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in voc.get_known_meanings(w=w,option=None) if m1 != ms]:
				self.inhibit(ms, w, voc)
			for w2 in [w3 for w3 in voc.get_known_words(m=ms,option=None) if w3 != w]:
				self.inhibit(ms, w2, voc)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ):
		if bool_succ:
			self.increase(ms, w, voc)
			for m in [m1 for m1 in voc.get_known_meanings(w=w,option=None) if m1 != mh]:
				self.inhibit(m, w, voc)
			for w2 in [w3 for w3 in voc.get_known_words(m=ms,option=None) if w3 != w]:
				self.inhibit(ms, w2, voc)
		voc.finish_update()
