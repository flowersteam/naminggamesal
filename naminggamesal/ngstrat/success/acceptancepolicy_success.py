
from ...ngmeth_utils.srtheo_utils import srtheo_voc

from .global_success import GlobalSuccessNoRandom

class AcceptancePolicySuccess(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		mem_new = mem.simulated_update_memory(ms=ms,w=w,mh=mh,voc=voc,role='both',bool_succ=True,context=context)
		voc2 = mem['interact_count_voc']
		voc2_new = mem_new['interact_count_voc']
		if srtheo_voc(voc,voc2_new)>=srtheo_voc(voc,voc2):
			return True
		else:
			return False

class AcceptancePolicyOrNormalSuccess(object):

	def eval(self, ms, w, mh, voc, mem, strategy, context=[]):
		succ_1 = GlobalSuccessNoRandom.eval(self, ms=ms, w=w, mh=mh, voc=voc, mem=mem, strategy=strategy, context=context)
		succ_2 = AcceptancePolicySuccess.eval(self, ms=ms, w=w, mh=mh, voc=voc, mem=mem, strategy=strategy, context=context)
		return (succ_1 or succ_2)