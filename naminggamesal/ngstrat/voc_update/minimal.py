from . import VocUpdate

class Minimal(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if bool_succ:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		voc.add(ms,w,context=context)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if bool_succ:
			voc.rm_syn(ms,w)
			voc.rm_hom(ms,w)
		voc.add(ms,w,context=context)
		voc.finish_update()


class MinimalSynOnly(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		if bool_succ:
			voc.rm_syn(ms,w)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		if bool_succ:
			voc.rm_syn(ms,w)
		voc.finish_update()


class MinimalPOne(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if not voc.exists(ms,w):
			voc.add(ms,w,val=0.1,context=context)
		if bool_succ:
			voc.add(ms,w,val=1,context=context)
			voc.rm_syn(ms,w)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if not voc.exists(ms,w):
			voc.add(ms,w,val=0.5,context=context)
		if bool_succ:
			voc.add(ms,w,val=1,context=context)
			voc.rm_syn(ms,w)
		voc.finish_update()
