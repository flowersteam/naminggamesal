import pytest
import copy

from naminggamesal import ngvoc

#voctype_list = list(ngvoc.voc_class.keys())
voctype_list = [
	'2dictdict',
	'matrix_new']


def test_importerror():
	try:
		a = ngvoc.get_vocabulary(voc_type='thereisnosuchclass')
	except ImportError as e:
		if len(e.args) and len(e.args[0])>14 and e.args[0][:15] == 'No such class: ':
			pass
		else:
			raise

@pytest.mark.parametrize("voc_type", voctype_list)
def test_import(voc_type):
	v = ngvoc.get_vocabulary(voc_type=voc_type)

@pytest.mark.parametrize("voc_type", voctype_list)
def test_discover_meanings(voc_type):
	m1 = 'ioh'
	m2 = 123
	m3 = 12
	m4= 'ohl'
	v = ngvoc.get_vocabulary(voc_type=voc_type)
	before = copy.deepcopy(v.accessible_meanings)
	v.discover_meanings([m1,m2,m3])
	between = copy.deepcopy(v.accessible_meanings)
	v.discover_meanings([m2,m4])
	after = copy.deepcopy(v.accessible_meanings)
	assert before == [] and between == [m1,m2,m3] and after == [m1,m2,m3,m4]

@pytest.mark.parametrize("voc_type", voctype_list)
def test_discover_words(voc_type):
	w1 = 'ioh'
	w2 = 123
	w3 = 12
	w4 = 'uig'
	v = ngvoc.get_vocabulary(voc_type=voc_type)
	before = copy.deepcopy(v.accessible_words)
	v.discover_words([w1,w2,w3])
	between = copy.deepcopy(v.accessible_words)
	v.discover_words([w2,w4])
	after = copy.deepcopy(v.accessible_words)
	assert before == [] and between == [w1,w2,w3] and after == [w1,w2,w3,w4]
