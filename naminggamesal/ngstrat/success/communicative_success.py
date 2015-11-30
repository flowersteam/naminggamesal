class CommunicativeSuccess(object):

	def eval(self, ms, w, mh, voc, strategy):
		if voc._content[ms,w] > 0:
			return True
		else:
			return False
