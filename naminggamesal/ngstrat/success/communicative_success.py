class CommunicativeSuccess(object):

	def eval(self, ms, w, mh, voc, strategy):
		if voc._content[ms,w] > 0:
			return True
		else:
			return False

class CommunicativeSuccessMax(object):

	def eval(self, ms, w, mh, voc, strategy):
		if w in voc.get_known_words(m=ms,option='max'):
			return True
		else:
			return False

