from . import VocUpdate

class Frequency(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ):
		y = 1./(2 - voc._content[ms, w]) # y = 1 - 1/(f+1)
		y = min(1,y)
		y = max(0,y)
		voc.add(ms,w,y) # f <- f+1

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ):
		voc.del_cache()
