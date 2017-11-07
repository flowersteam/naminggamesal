import pytest
import copy

from naminggamesal import ngvoc

#voctype_list = list(ngvoc.voc_class.keys())
voctype_list = [
	'2dictdict',
	'pandas',
	'matrix_new']

@pytest.mark.parametrize("voc_type", voctype_list)
def test_import(voc_type):
	v = ngvoc.get_vocabulary(voc_type=voc_type)

@pytest.fixture(params=voctype_list)
def tempvoc(request):
	param = request.param
	return ngvoc.get_vocabulary(voc_type=param)


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

