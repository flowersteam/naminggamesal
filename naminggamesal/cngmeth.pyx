from .ngmeth import srtheo_voc
import copy
from libcpp.vector cimport vector

def srtheo_voc_membased(voc1,voc2=None,voc2_m=None,voc2_w=None,m=None,w=None,role='both'):
	if hasattr(voc1,'get_alterable_shallow_copy'):
		voc1_temp = voc1.get_alterable_shallow_copy()
	else:
		voc1_temp = copy.deepcopy(voc1)
	cdef int i_m1,i_w1
	cdef int KM,KW
	cdef vector l_KM,l_KW
	l_KM = voc1_temp.get_known_meanings()
	KM = len(l_KM)
	for i_m1 in range(KM) :
		m1 = l_KM[i_m1]
		l_KW = voc1_temp.get_known_words(m=m1)
		KW = len(l_KW)
		for i_w1 in range(KW):
			w1 = l_KW[i_w1]
			val_temp = voc2.get_value(m=m1,w=w1,content_type='m')
			val_temp = max(val_temp, 0.000001)
			voc1_temp.add(m=m1,w=w1,val=val_temp,content_type='m')


	l_KW = voc1_temp.get_known_words()
	KW = len(l_KW)
	for i_w1 in range(KW):
		w1 = l_KW[i_w1]
		l_KM = voc1_temp.get_known_meanings(w=w1)
		KM = len(l_KM)
		for i_m1 in range(KM) :
			m1 = l_KM[i_m1]
			val_temp = voc2.get_value(m=m1,w=w1,content_type='w')
			val_temp = max(val_temp, 0.000001)
			voc1_temp.add(m=m1,w=w1,val=val_temp,content_type='w')

	return srtheo_voc(voc1=voc1_temp,voc2=voc2,voc2_m=voc2_m,voc2_w=voc2_w,m=m,w=w,role=role)
