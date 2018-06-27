class AlignmentSuccess(object):

	def eval(self, ms, w, mh, voc, mem, strategy,context=[]):
		if voc.exists(ms,w) and strategy.pick_w(m=ms,voc=voc,mem=mem,context=context) == w:
			return True
		else:
			return False

