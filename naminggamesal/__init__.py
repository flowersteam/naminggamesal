from ._version import __version__

from . import ngdb
from . import ngsimu
from . import ngmeth

import additional.custom_func as custom_func

def get_allfunc(tags=[],level=None):
	def test(f):
		f_obj = getattr(ngmeth,f)
		t1 = (f_obj.__class__ == custom_func.CustomFunc)
		t1 = t1 and tags == f_obj.tags
		if level is not None:
			t1 = t1 and f_obj.level == level
		return t1
	return [f for f in dir(ngmeth) if test(f)]

