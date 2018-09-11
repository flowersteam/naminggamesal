from ._version import __version__

from . import ngdb
from . import ngsimu
from . import ngmeth

from .tools import custom_func

def get_allfunc(tags=[],level=None):
	def test(f):
		f_obj = getattr(ngmeth,f)
		t1 = (f_obj.__class__ == custom_func.CustomFunc)
		t1 = t1 and tags == f_obj.tags
		if level is not None:
			t1 = t1 and f_obj.level == level
		return t1
	def truncate(f):
		ans = f[7:]
		if f[-5:] == '_mean':
			ans = ans[:-5]
		return ans
	return [ truncate(f) for f in dir(ngmeth) if test(f)]

DEBUG_MODE = False
