import pytest
import copy

from naminggamesal import ngvoc

#voctype_list = list(ngvoc.voc_class.keys())
voctype_list = [
	'2dictdict',
	#'pandas',
	'matrix_new']

@pytest.mark.parametrize("voc_type", voctype_list)
def test_import(voc_type):
	v = ngvoc.get_vocabulary(voc_type=voc_type)

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


def test_importerror():
	try:
		a = ngvoc.get_vocabulary(voc_type='thereisnosuchclass')
	except ImportError as e:
		if len(e.args) and len(e.args[0])>14 and e.args[0][:15] == 'No such class: ':
			pass
		else:
			raise

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