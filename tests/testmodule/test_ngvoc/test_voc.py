import pytest
import copy
import random
import numpy as np

from naminggamesal import ngvoc,ngmeth

#voctype_list = list(ngvoc.voc_class.keys())
voctype_list = [
	'2dictdict',
	#'pandas',
	'matrix_new',
	'sparse_new',
	]

@pytest.mark.parametrize("voc_type", voctype_list)
def test_import(voc_type):
	v = ngvoc.get_vocabulary(voc_type=voc_type)

def test_importerror():
	try:
		a = ngvoc.get_vocabulary(voc_type='thereisnosuchclass')
	except ImportError as e:
		if len(e.args) and len(e.args[0])>14 and e.args[0][:15] == 'No such class: ':
			pass
		else:
			raise

@pytest.fixture(params=voctype_list)
def tempvoc(request):
	param = request.param
	return ngvoc.get_vocabulary(voc_type=param)

@pytest.fixture(params=voctype_list)
def tempvoc2(request):
	param = request.param
	v = ngvoc.get_vocabulary(voc_type=param)
	meanings = ['a','b','c','d','e','f']
	words = range(-4,10)
	v.discover_meanings(meanings)
	v.discover_words(words)
	assoc_list = [
			('a',0),
			('b',0),
			('a',1),
			('e',9),
			('c',1),
			('d',1),
			]
	for assoc in assoc_list:
		v.add(m=assoc[0],w=assoc[1])
	v.assoc_list = assoc_list
	return v

@pytest.fixture(params=voctype_list)
def tempvoc3(request):
	param = request.param
	v = ngvoc.get_vocabulary(voc_type=param)
	meanings = ['a','b','c','d','e','f']
	words = range(-4,10)
	v.discover_meanings(meanings)
	v.discover_words(words)
	assoc_list = [ (random.choice(meanings),random.choice(words)) for i in range(25)]
	for assoc in assoc_list:
		v.add(m=assoc[0],w=assoc[1])
	v.assoc_list = assoc_list
	return v

@pytest.fixture(params=voctype_list)
def tempvoc4(request):
	param = request.param
	v = ngvoc.get_vocabulary(voc_type=param)
	meanings = ['a','b','c','d','e','f']
	words = range(-4,10)
	v.discover_meanings(meanings)
	v.discover_words(words)
	assoc_list = [ (random.choice(meanings),random.choice(words)) for i in range(25)]
	for assoc in assoc_list:
		v.add(m=assoc[0],w=assoc[1],val=round(random.random(),3))
	v.assoc_list = assoc_list
	return v

@pytest.fixture(params=voctype_list)
def tempvoc5(request):
	param = request.param
	v = ngvoc.get_vocabulary(voc_type=param)
	meanings = ['a','b','c','d','e','f']
	words = range(-4,10)
	v.discover_meanings(meanings)
	v.discover_words(words)
	assoc_list = [ (random.choice(meanings),random.choice(words)) for i in range(25)]
	for assoc in assoc_list:
		v.add(m=assoc[0],w=assoc[1],val=round(random.random(),3))
	v.assoc_list = assoc_list
	return v


@pytest.fixture(params=voctype_list)
def tempvoc6(request):
	param = request.param
	v = ngvoc.get_vocabulary(voc_type=param)
	meanings = ['a','b','c','d','e','f']
	words = range(-4,10)
	v.discover_meanings(meanings)
	v.discover_words(words)
	assoc_list = [ (random.choice(meanings),random.choice(words)) for i in range(25)]
	for assoc in assoc_list:
		v.add(m=assoc[0],w=assoc[1],val=random.random())
	v.assoc_list = assoc_list
	return v

@pytest.fixture(params=voctype_list)
def tempvoc7(request):
	param = request.param
	v = ngvoc.get_vocabulary(voc_type=param)
	meanings = ['a','b','c','d','e','f']
	words = range(-4,10)
	v.discover_meanings(meanings)
	v.discover_words(words)
	assoc_list = [ (random.choice(meanings),random.choice(words)) for i in range(25)]
	for assoc in assoc_list:
		v.add(m=assoc[0],w=assoc[1],val=random.random())
	v.assoc_list = assoc_list
	return v


def test_discover_meanings(tempvoc):
	m1 = 'ioh'
	m2 = 123
	m3 = 12
	m4= 'ohl'
	v = tempvoc
	before = copy.deepcopy(v.accessible_meanings)
	v.discover_meanings([m1,m2,m3])
	between = copy.deepcopy(v.accessible_meanings)
	v.discover_meanings([m2,m4])
	after = copy.deepcopy(v.accessible_meanings)
	assert before == [] and between == [m1,m2,m3] and after == [m1,m2,m3,m4]

def test_discover_words(tempvoc):
	w1 = 'ioh'
	w2 = 123
	w3 = 12
	w4 = 'uig'
	v = tempvoc
	before = copy.deepcopy(v.accessible_words)
	v.discover_words([w1,w2,w3])
	between = copy.deepcopy(v.accessible_words)
	v.discover_words([w2,w4])
	after = copy.deepcopy(v.accessible_words)
	assert before == [] and between == [w1,w2,w3] and after == [w1,w2,w3,w4]


def test_add(tempvoc):
	w = 'a'
	m = 123
	v = tempvoc
	v.discover_words([w])
	v.discover_meanings([m])
	before = v.get_value(m=m,w=w)
	v.add(m=m,w=w,val = 0.75)
	after = v.get_value(m=m,w=w)
	assert before == 0 and after == 0.75


def test_add2(tempvoc):
	w = 'a'
	m = 123
	v = tempvoc
	v.discover_words([w])
	v.discover_meanings([m])
	before = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.add(m=m,w=w,val = 0.75,content_type='m')
	v.add(m=m,w=w,val = 0.95,content_type='w')
	after = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	assert before == (0,0) and after == (0.75,0.95)


def test_add3(tempvoc):
	w = 'a'
	m = 123
	v = tempvoc
	v.discover_words([w])
	v.discover_meanings([m])
	before = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.add(m=m,w=w,val = 0.85,content_type='both')
	after = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	assert before == (0,0) and after == (0.85,0.85)


def test_add4(tempvoc):
	w = 'a'
	m = 123
	v = tempvoc
	v.discover_words([w])
	v.discover_meanings([m])
	before = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.add(m=m,w=w,val = 0.85,content_type='both')
	between = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.add(m=m,w=w,val = -0.6,content_type='both')
	after = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	assert before == (0,0) and between == (0.85,0.85) and after == (0,0)


def test_rm(tempvoc):
	w = 'a'
	m = 123
	v = tempvoc
	v.discover_words([w])
	v.discover_meanings([m])
	v.add(m=m,w=w,val = 0.75)
	before = v.get_value(m=m,w=w)
	v.rm(m=m,w=w)
	after = v.get_value(m=m,w=w)
	assert after == 0 and before == 0.75

def test_rm2(tempvoc):
	w = 'a'
	m = 123
	v = tempvoc
	v.discover_words([w])
	v.discover_meanings([m])
	v.add(m=m,w=w,val = 0.75)
	before = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.rm(m=m,w=w,content_type='both')
	before2 = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.add(m=m,w=w,val = 0.75)
	v.rm(m=m,w=w,content_type='m')
	after = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	v.rm(m=m,w=w,content_type='w')
	after2 = v.get_value(m=m,w=w,content_type='m'),v.get_value(m=m,w=w,content_type='w')
	assert after2 == (0,0)  and after == (0,0.75) and before == (0.75,0.75) and before2 == (0,0)

def test_getM(tempvoc2):
	assert tempvoc2.get_M() == 6

def test_getM2(tempvoc2):
	tempvoc2.discover_meanings(['bb','rr'])
	assert tempvoc2.get_M() == 8

def test_getW(tempvoc2):
	assert tempvoc2.get_W() == 14

def test_getW2(tempvoc2):
	tempvoc2.discover_words([123456,123,456])
	assert tempvoc2.get_W() == 17


def test_getknown_words(tempvoc2):
	v = tempvoc2
	assert sorted(v.get_known_words())==[0,1,9] and sorted(v.get_known_words(m='a')) == [0,1]

def test_getknown_meanings(tempvoc2):
	v = tempvoc2
	assert sorted(v.get_known_meanings())==['a','b','c','d','e'] and sorted(v.get_known_meanings(w=0)) == ['a','b']



def Nlink(voc):
	ans = 0
	for m in voc.get_known_meanings():
		ans += len(voc.get_known_words(m=m))
	return ans


def test_rmsyn(tempvoc2):
	v = tempvoc2
	m='a'
	w=3
	before = Nlink(v)
	v.rm_syn(m=m,w=w)
	after = Nlink(v)
	assert before == len(v.assoc_list) and after == len(v.assoc_list)-2 and v.get_value(m=m,w=0) == 0 and v.get_value(m=m,w=1) == 0

def test_rmhom(tempvoc2):
	v = tempvoc2
	m='f'
	w=1
	before = Nlink(v)
	v.rm_hom(m=m,w=w)
	after = Nlink(v)
	assert before == len(v.assoc_list) and after == len(v.assoc_list)-3 and v.get_value(m='a',w=w) == 0 and v.get_value(m='c',w=w) == 0 and v.get_value(m='d',w=w) == 0

def test_rmsyn2(tempvoc2):
	v = tempvoc2
	m='a'
	w=1
	before = Nlink(v)
	v.rm_syn(m=m,w=w)
	after = Nlink(v)
	assert before == len(v.assoc_list) and after == len(v.assoc_list)-1 and v.get_value(m=m,w=0) == 0 and v.get_value(m=m,w=1) == 1

def test_rmhom2(tempvoc2):
	v = tempvoc2
	m='d'
	w=1
	before = Nlink(v)
	v.rm_hom(m=m,w=w)
	after = Nlink(v)
	assert before == len(v.assoc_list) and after == len(v.assoc_list)-2 and v.get_value(m='a',w=w) == 0 and v.get_value(m='c',w=w) == 0 and v.get_value(m='d',w=w) == 1






epsilon = 10**-10

def test_srtheovoc_basic(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=1,content_type='m')
	assert ngmeth.srtheo_voc(v,v) == 0

def test_srtheovoc_basic2(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=1,content_type='w')
	assert ngmeth.srtheo_voc(v,v) == 0

def test_srtheovoc_basic3(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=1,content_type='both')
	assert ngmeth.srtheo_voc(v,v) == 1/3.

def test_srtheovoc_basic4(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='m')
	v.add(m='a',w=1,content_type='m')
	v.add(m='a',w=2,content_type='m')
	v.add(m='a',w=3,content_type='m')
	v.add(m='a',w=1,content_type='w')
	assert ngmeth.srtheo_voc(v,v) == 1/12.

def test_srtheovoc_basic4_2(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='m')
	v.add(m='a',w=1,content_type='m')
	v.add(m='a',w=1,content_type='w')
	assert ngmeth.srtheo_voc(v,v) == 1/6.

def test_srtheovoc_basic5(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='w')
	v.add(m='a',w=1,content_type='w')
	v.add(m='a',w=2,content_type='w')
	v.add(m='a',w=3,content_type='w')
	v.add(m='a',w=1,content_type='m')
	assert ngmeth.srtheo_voc(v,v) == 1/3.

def test_srtheovoc_basic5_2(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='w')
	v.add(m='a',w=1,content_type='w')
	v.add(m='a',w=1,content_type='m')
	assert ngmeth.srtheo_voc(v,v) == 1/3.

def test_srtheovoc_basic6(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='w')
	v.add(m='a',w=1,content_type='w')
	v.add(m='b',w=0,content_type='w')
	v.add(m='a',w=0,content_type='m')
	v.add(m='a',w=1,content_type='m')
	v.add(m='b',w=0,content_type='m')
	assert abs(ngmeth.srtheo_voc(v,v) - 5/12.) < epsilon

def test_srtheovoc_basic6_2(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='w')
	v.add(m='a',w=1,content_type='w')
	v.add(m='b',w=0,content_type='w')
	v.add(m='a',w=0,content_type='m')
	v.add(m='b',w=0,content_type='m')
	assert abs(ngmeth.srtheo_voc(v,v) - 4/12.) < epsilon

def test_srtheovoc_basic6_3(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v2 = copy.deepcopy(v)
	v.add(m='a',w=0,content_type='both')
	v.add(m='a',w=1,content_type='both')
	v.add(m='b',w=0,content_type='both')
	v2.add(m='a',w=0,content_type='both')
	v2.add(m='b',w=1,content_type='both')
	v2.add(m='c',w=2,content_type='both')
	v2.add(m='b',w=2,content_type='both')
	assert abs(ngmeth.srtheo_voc(v,v2,role='speaker') - 1/6.) < epsilon

def test_srtheovoc_basic6_3bis(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v2 = copy.deepcopy(v)
	v.add(m='a',w=0,content_type='both')
	v.add(m='a',w=1,content_type='both')
	v.add(m='b',w=0,content_type='both')
	v2.add(m='a',w=0,content_type='both')
	v2.add(m='b',w=1,content_type='both')
	v2.add(m='c',w=2,content_type='both')
	v2.add(m='b',w=2,content_type='both')
	assert abs(ngmeth.srtheo_voc(v,v2,role='hearer') - 1/6.) < epsilon

def test_srtheovoc_basic7(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	for m in ['a','b','c']:
		for w in range(4):
			v.add(m=m,w=w,content_type='both')
	assert abs(ngmeth.srtheo_voc(v,v) - 1/3.) < epsilon

role_list = [
	'speaker',
	'hearer',
	'both'
	]


@pytest.mark.parametrize("role", role_list)
def test_srtheovoc(tempvoc2,role):
	v = tempvoc2
	v2 = tempvoc2
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc2(tempvoc3,role):
	v = tempvoc3
	v2 = tempvoc3
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc3(tempvoc2,tempvoc3,role):
	v = tempvoc2
	v2 = tempvoc3
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc4(tempvoc4,role):
	v = tempvoc4
	v2 = tempvoc4
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc5(tempvoc3,tempvoc4,role):
	v = tempvoc3
	v2 = tempvoc4
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc6(tempvoc5,tempvoc4,role):
	v = tempvoc5
	v2 = tempvoc4
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc7(tempvoc6,tempvoc7,role):
	v = tempvoc6
	v2 = tempvoc7
	assert abs(ngmeth.srtheo_voc(v,v2,role=role) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role)) < epsilon


def test_weightvalues_m(tempvoc2):
	v = tempvoc2
	assert sum(v.get_known_words_weights_values(m='a')) == 2

def test_weightvalues_w(tempvoc2):
	v = tempvoc2
	assert sum(v.get_known_meanings_weights_values(w=1)) == 3




def test_norm_0(tempvoc2):
	m1 = tempvoc2._content_m
	if hasattr(tempvoc2.__class__,'norm'):
		m2 = np.zeros((6,14))
		for x,y,val in [
			(0,4 ,0.5),
			(1,4 ,0.5),
			(0,5 ,1/3.),
			(4,13 ,1),
			(2,5 ,1./3),
			(3,5 ,1/3.),
			]:
			m2[x,y] = val
		assert (tempvoc2.__class__.norm(m1,axis=0) == m2).all()

def test_norm_1(tempvoc2):
	if hasattr(tempvoc2.__class__,'norm'):
		m1 = tempvoc2._content_m
		m2 = np.zeros((6,14))
		for x,y,val in [
			(0,4 ,0.5),
			(1,4 ,1),
			(0,5 ,0.5),
			(4,13 ,1),
			(2,5 ,1.),
			(3,5 ,1),
			]:
			m2[x,y] = val
		assert (tempvoc2.__class__.norm(m1,axis=1) == m2).all()

def test_multsum(tempvoc2):
	if hasattr(tempvoc2.__class__,'mult_sum'):
		m1 = tempvoc2._content_m
		assert tempvoc2.__class__.mult_sum(m1,m1) == 6



def test_srtheovoc_m(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='m')
	v.add(m='a',w=1,content_type='m')
	v.add(m='a',w=2,content_type='m')
	v.add(m='a',w=3,content_type='m')
	v.add(m='a',w=1,content_type='w')
	assert ngmeth.srtheo_voc(v,v,m='a') == 1/4.

def test_srtheovoc_m2(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='m')
	v.add(m='a',w=1,content_type='m')
	v.add(m='a',w=2,content_type='m')
	v.add(m='a',w=3,content_type='m')
	v.add(m='a',w=1,content_type='w')
	assert ngmeth.srtheo_voc(v,v,m='b') == 0.

def test_srtheovoc_m3(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='m')
	v.add(m='a',w=1,content_type='m')
	v.add(m='a',w=2,content_type='m')
	v.add(m='b',w=0,content_type='m')
	v.add(m='a',w=1,content_type='w')
	v.add(m='b',w=1,content_type='w')
	assert ngmeth.srtheo_voc(v,v,m='a') == 1/6. and ngmeth.srtheo_voc(v,v,m='b') == 0.

def test_srtheovoc_m4(tempvoc):
	v = tempvoc
	v.discover_meanings(['a','b','c'])
	v.discover_words(range(4))
	v.add(m='a',w=0,content_type='w')
	v.add(m='a',w=1,content_type='w')
	v.add(m='a',w=2,content_type='w')
	v.add(m='b',w=0,content_type='w')
	v.add(m='a',w=1,content_type='m')
	v.add(m='b',w=1,content_type='m')
	assert ngmeth.srtheo_voc(v,v,m='a') == 1. and ngmeth.srtheo_voc(v,v,m='b') == 0.

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc8(tempvoc6,tempvoc7,role):
	v = tempvoc6
	v2 = tempvoc7
	m = v.get_random_known_m(option=None)
	assert abs(ngmeth.srtheo_voc(v,v2,role=role,m=m) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role,m=m)) < epsilon

@pytest.mark.parametrize("role", role_list)
def test_srtheovoc9(tempvoc6,tempvoc7,role):
	v = tempvoc6
	v2 = tempvoc7
	m = v.get_random_known_m(option=None)
	w = v.get_random_known_w(m=m,option=None)
	assert abs(ngmeth.srtheo_voc(v,v2,role=role,m=m,w=w) - ngmeth.srtheo_voc(v,v2,force_ngmeth=True,role=role,m=m,w=w)) < epsilon
