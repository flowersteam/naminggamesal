#==================


def srtheo_voc_old(voc1,voc2=None,voc2_m=None,voc2_w=None,m=None,w=None,role='both',force_ngmeth=False):
	if (not force_ngmeth) and voc2 is not None and hasattr(voc1.__class__,'srtheo_voc') and hasattr(voc2.__class__,'srtheo_voc') and voc1.__class__.srtheo_voc == voc2.__class__.srtheo_voc:
		return voc1.srtheo_voc(voc1=voc1,voc2=voc2,m=m,w=w,role=role)
	ans = 0.
	if not hasattr(voc1,'_content_m'):
		if role == 'both' or role == 'hearer':
			m1 = copy.deepcopy(voc1)
			if voc2 is not None:
				m2 = copy.deepcopy(voc2)
			else:
				m2 = copy.deepcopy(voc2_m)

			if m is not None:
				m2 = m2[m,:]
				m1 = m1[m,:]
			if w is not None:
				m1 = m1[:,w]
				m2 = m2[:,w]

#			if renorm:
#				if renorm_fact is None: # !!!!! TODO: Deal with div by zero
			m1 = m1 / np.linalg.norm(m1, axis=0, ord=1,keepdims=True)
#					m2 = m2 / np.linalg.norm(m2, axis=1, ord=1,keepdims=True)
#				else:# !!!!! TODO: Deal with div by zero
#					m1 = m1 / renorm_fact
#					m2 = m2 / renorm_fact
			mult = np.multiply(m1,m2)
			ans += 1./voc1.shape[0] * np.nan_to_num(mult).sum()
		if role == 'both' or role == 'speaker':
			m1 = copy.deepcopy(voc1)
			if voc2 is not None:
				m2 = copy.deepcopy(voc2)
			else:
				m2 = copy.deepcopy(voc2_w)

			if m is not None:
				m2 = m2[m,:]
				m1 = m1[m,:]
			if w is not None:
				m1 = m1[:,w]
				m2 = m2[:,w]

#			if renorm:
#				if renorm_fact is None:# !!!!! TODO: Deal with div by zero
			m1 = m1 / np.linalg.norm(m1, axis=1, ord=1,keepdims=True)
#					m2 = m2 / np.linalg.norm(m2, axis=0, ord=1,keepdims=True)
#				else:
#					m1 = m1 / renorm_fact# !!!!! TODO: Deal with div by zero
#					m2 = m2 / renorm_fact
			mult = np.multiply(m1,m2)
			ans += 1./voc1.shape[0] * np.nan_to_num(mult).sum()
	else:
		if role == 'both' or role == 'speaker':
			if m is not None and w is None:# or w is not None:
				if m in voc1.get_known_meanings(option=None):#voc1._content_m.keys():
					for w1 in voc1.get_known_words(m=m,option=None):#voc1._content_m[m].keys():
						if len(voc1.get_known_words(m=m)):
							ans += voc1.get_value(m,w1,content_type='m') * voc2.get_value(m,w1,content_type='w')/(float(sum(voc1.get_known_words_weights_values(m=m))))#/float(voc1.get_M())#/float(len(voc2.get_known_words(m=m))*len(voc1.get_known_meanings(w=w1)))#voc1._content_m[m][w1] * voc2._content_w[w1][m]
			elif m is not None and w is not None:
				if len(voc1.get_known_words(m=m)):
					ans += voc1.get_value(m,w,content_type='m') * voc2.get_value(m,w,content_type='w')/(float(sum(voc1.get_known_words_weights_values(m=m))))#/float(voc1.get_M())#/float(len(voc2.get_known_words(m=m))*len(voc1.get_known_meanings(w=w1)))#voc1._content_m[m][w1] * voc2._content_w[w1][m]
			elif m is None and w is not None:
				for m1 in voc1.get_known_meanings(w=w,option=None):
					if len(voc1.get_known_words(m=m1)) and voc1.get_M():
						ans += voc1.get_value(m1,w,content_type='m') * voc2.get_value(m1,w,content_type='w')/(float(sum(voc1.get_known_words_weights_values(m=m1)))*float(voc1.get_M()))#/float(len(voc2.get_known_words(m=m1))*len(voc1.get_known_meanings(w=w1)))
			else:
				for m1 in voc1.get_known_meanings(option=None):
					for w1 in voc1.get_known_words(m=m1,option=None):
						if len(voc1.get_known_words(m=m1)) and voc1.get_M():
							try:
								if not hasattr(voc2,'is_normalized') or not voc2.is_normalized:
									ans += voc1.get_value(m1,w1,content_type='m') * voc2.get_value(m1,w1,content_type='w')/(float(sum(voc1.get_known_words_weights_values(m=m1)))*sum(voc1.get_known_meanings_weights_values(w=w1))*float(voc1.get_M()))#/float(len(voc2.get_known_words(m=m1))*len(voc1.get_known_meanings(w=w1)))
								else:
									ans += voc1.get_value(m1,w1,content_type='m') * voc2.get_value(m1,w1,content_type='w')/(float(sum(voc1.get_known_words_weights_values(m=m1)))*float(voc1.get_M()))#/float(len(voc2.get_known_words(m=m1))*len(voc1.get_known_meanings(w=w1)))
							except ZeroDivisionError :
								pass
		if role == 'both' or role == 'hearer':
			if w is not None and m is None:# or m is not None:
				if w in voc1.get_known_words(option=None): #voc2._content_w.keys():
					for m1 in voc1.get_known_meanings(w=w,option=None): #voc2._content_w[w].keys():
						if len(voc1.get_known_meanings(w=w)) and voc2.get_M():
							ans += voc2.get_value(m1,w,content_type='m') * voc1.get_value(m1,w,content_type='w')/(float(sum(voc1.get_known_meanings_weights_values(w=w)))*float(voc2.get_M()))#/float(len(voc1.get_known_words(m=m1))*len(voc2.get_known_meanings(w=w)))#voc1._content_m[m1][w] * voc2._content_w[w][m1]
			elif w is not None and m is not None:
				if len(voc1.get_known_meanings(w=w)):
					ans += voc2.get_value(m,w,content_type='m') * voc1.get_value(m,w,content_type='w')/(float(sum(voc1.get_known_meanings_weights_values(w=w))))#/float(voc2.get_M())
			elif w is None and m is not None:
				for w1 in voc2.get_known_words(m=m,option=None):
					if len(voc1.get_known_meanings(w=w1)):
						ans += voc2.get_value(m,w1,content_type='m') * voc1.get_value(m,w1,content_type='w')/(float(sum(voc1.get_known_meanings_weights_values(w=w1))))#/float(voc2.get_M())
			else:
				for m1 in voc2.get_known_meanings(option=None):
					for w1 in voc2.get_known_words(m=m1,option=None):
						if len(voc1.get_known_meanings(w=w1)) and voc2.get_M():
							ans += voc2.get_value(m1,w1,content_type='m') * voc1.get_value(m1,w1,content_type='w')/(float(sum(voc1.get_known_meanings_weights_values(w=w1)))*float(voc2.get_M()))#/float(len(voc1.get_known_words(m=m1))*len(voc2.get_known_meanings(w=w1)))
	if role == 'both':
		return ans/2.
	else:
		return ans

def srtheo_voc(voc1,voc2=None,m=None,w=None,role='both',force_ngmeth=False):
	if (not force_ngmeth) and voc2 is not None and hasattr(voc1.__class__,'srtheo_voc') and hasattr(voc2.__class__,'srtheo_voc') and voc1.__class__.srtheo_voc == voc2.__class__.srtheo_voc:
		return voc1.srtheo_voc(voc1=voc1,voc2=voc2,m=m,w=w,role=role)
	if role == 'speaker':
		ans = 0
		if m is not None and w is None:
			if m in voc1.get_known_meanings(option=None):
				for w1 in voc1.get_known_words(m=m,option=None):
					try:
						prefactor = 1.
						if not hasattr(voc2,'is_normalized') or not voc2.is_normalized:
							prefactor *= 1./sum(voc2.get_known_meanings_weights_values(w=w1))
						if not hasattr(voc1,'is_normalized') or not voc1.is_normalized:
							prefactor *= 1./sum(voc1.get_known_words_weights_values(m=m))
						if len(voc1.get_known_words(m=m)):
							ans += prefactor*voc1.get_value(m,w1,content_type='m') * voc2.get_value(m,w1,content_type='w')
					except ZeroDivisionError:
						pass
		elif m is not None and w is not None:
			try:
				prefactor = 1.
				if not hasattr(voc2,'is_normalized') or not voc2.is_normalized:
					prefactor *= 1./sum(voc2.get_known_meanings_weights_values(w=w))
				if not hasattr(voc1,'is_normalized') or not voc1.is_normalized:
					prefactor *= 1./sum(voc1.get_known_words_weights_values(m=m))
				if len(voc1.get_known_words(m=m)):
					ans += prefactor*voc1.get_value(m,w,content_type='m') * voc2.get_value(m,w,content_type='w')
			except ZeroDivisionError:
				pass
		elif m is None and w is not None:
			raise NotImplementedError
		else:
			for m1 in voc1.get_known_meanings(option=None):
				for w1 in voc1.get_known_words(m=m1,option=None):
					if len(voc1.get_known_words(m=m1,option=None)) and voc1.get_M():
						try:
							prefactor = 1.
							if not hasattr(voc2,'is_normalized') or not voc2.is_normalized:
								prefactor *= 1./sum(voc2.get_known_meanings_weights_values(w=w1))
							if not hasattr(voc1,'is_normalized') or not voc1.is_normalized:
								prefactor *= 1./sum(voc1.get_known_words_weights_values(m=m1))
							ans += prefactor * voc1.get_value(m1,w1,content_type='m') * voc2.get_value(m1,w1,content_type='w')/len(voc1.accessible_meanings)#float(voc1.get_M())
						except ZeroDivisionError :
							pass
		return ans
	if role == 'hearer':
		return srtheo_voc(voc1=voc2,voc2=voc1,m=m,w=w,role='speaker',force_ngmeth=force_ngmeth)
	if role == 'both':
		return (srtheo_voc(voc1=voc1,voc2=voc2,m=m,w=w,role='speaker',force_ngmeth=force_ngmeth)+srtheo_voc(voc1=voc1,voc2=voc2,m=m,w=w,role='hearer',force_ngmeth=force_ngmeth))/2.
	else:
		raise NotImplementedError('Unknow role: '+str(role))

import pyximport; pyximport.install()
from .csrtheo_utils import srtheo_voc_membased
