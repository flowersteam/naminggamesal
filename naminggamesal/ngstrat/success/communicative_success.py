class CommunicativeSuccess(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		if voc.exists(ms,w):
			return True
		else:
			return False

class CommunicativeSuccessMax(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		if w in voc.get_known_words(m=ms,option='max'):
			return True
		else:
			return False

