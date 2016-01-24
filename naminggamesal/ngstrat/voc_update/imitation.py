from . import VocUpdate

class Imitation(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)
		voc.finish_update()
