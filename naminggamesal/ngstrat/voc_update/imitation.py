from . import VocUpdate
import random

class Imitation(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.add(ms,w,context=context)
		print voc._content_m.index.levels
		voc.rm_hom(ms,w)
		print voc._content_m.index.levels
		voc.rm_syn(ms,w)
		print voc._content_m.index.levels
		voc.finish_update()
		print voc._content_m.index.levels

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		print voc._content_m.index.levels
		voc.add(ms,w,context=context)
		print voc._content_m.index.levels
		voc.rm_hom(ms,w)
		print voc._content_m.index.levels
		voc.rm_syn(ms,w)
		print voc._content_m.index.levels
		voc.finish_update()
		print voc._content_m.index.levels

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
