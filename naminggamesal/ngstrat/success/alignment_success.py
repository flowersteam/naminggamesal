class AlignmentSuccess(object):

	def eval(self, ms, w, mh, voc, strategy):
		if voc.get_content()[ms,w] > 0 and strategy.pick_w(m=ms,voc=voc) == w:
			return True
		else:
			return False
