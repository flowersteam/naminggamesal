
class GlobalSuccess(object):

	def eval(self, ms, w, mh, voc, strategy, context=[]):
		if ms == mh:
			return True
		else:
			return False

class GlobalSuccessRestrictive(object):

	def eval(self, ms, w, mh, voc, strategy, context=[]):
		if [mh] == voc.get_known_meanings(w=w,option='max'):
			return True
		else:
			return False
