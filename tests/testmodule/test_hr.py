import pytest

import naminggamesal as ngal
from naminggamesal.tools import holedrange


@pytest.fixture
def hr(request):
	return holedrange.HoledRange(5)

def test_add(hr):
	for a in range(5):
		assert a in hr

	hr.append(5)
	for a in range(6):
		assert a in hr
	assert len(hr) == 6

def test_remove(hr):
	hr.remove(3)
	for a in [0,1,2,4]:
		assert a in hr
	assert 3 not in hr
	assert len(hr) == 4

def test_remove0(hr):
	hr.remove(0)
	for a in [3,1,2,4]:
		assert a in hr
	assert 0 not in hr
	assert len(hr) == 4
	assert set([a for a in hr]) == set([1,2,3,4])


def test_add2(hr):
	for a in range(5):
		assert a in hr

	hr.append(15)
	for a in [0,1,2,3,4,15]:
		assert a in hr
	assert len(hr) == 6

	assert [a for a in hr] == [0,1,2,3,4,15]
