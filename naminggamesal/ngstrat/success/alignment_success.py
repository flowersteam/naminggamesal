class AlignmentSuccess(object):

	def eval(self, ms, w, mh, voc, strategy,context=[]):
		if voc.exists(ms,w) and strategy.pick_w(m=ms,voc=voc) == w:
			return True
		else:
			return False
