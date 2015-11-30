class AlignmentSuccess(object):

	def eval(self, ms, w, mh, voc, strategy):
		if voc._content[ms,w] > 0 and strategy.pick_w(m=ms,voc=voc) == w:
			return True
		else:
			return False
