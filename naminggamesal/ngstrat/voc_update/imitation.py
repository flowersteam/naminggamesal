from . import VocUpdate
import random

class Imitation(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		voc.rm_hom(ms,w)
		voc.rm_syn(ms,w)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		voc.rm_hom(ms,w)
		voc.rm_syn(ms,w)
		voc.finish_update()

class ImitationPermutation(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		if not bool_succ and len(voc.get_known_words(ms)):
			wh = random.choice(voc.get_known_words(ms))
			voc.add(mh,wh,context=context)
		voc.add(ms,w,context=context)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		voc.rm_syn(ms,w)
		voc.rm_hom(ms,w)
		voc.finish_update()
