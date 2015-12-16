from . import VocUpdate

class Imitation(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ):
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)
		voc.add(ms,w,1)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ):
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)
		voc.add(ms,w,1)
		voc.finish_update()
