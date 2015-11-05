from . import VocUpdate

class Frequency(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem):
		y = 1./(2 - voc.get_content()[ms, w]) # y = 1 - 1/(f+1)
		voc.add(ms,w,y) # f <- f+1

	def update_speaker(self,ms,w,mh,voc,mem):
		pass
