from . import VocUpdate

class Minimal(VocUpdate):

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