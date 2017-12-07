
class GlobalSuccess(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		if ms == mh:
			return True
		else:
			return False

class GlobalSuccessRestrictive(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		if [mh] == voc.get_known_meanings(w=w,option='max'):
			return True
		else:
			return False


class GlobalSuccessEpirob(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		if ms == mh or not voc.get_known_meanings(w):
			return True
		else:
			return False


class GlobalSuccessNoRandom(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		if ms == mh and ms in voc.get_known_meanings(w):
			return True
		else:
			return False