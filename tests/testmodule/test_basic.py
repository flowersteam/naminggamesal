import os
import importlib

def test_basic():
	assert True

def test_import():
	path = os.path.abspath(__file__)
	dir_name = os.path.dirname(os.path.dirname(os.path.dirname(path)))
	libname = os.path.basename(dir_name)
	importlib.import_module(libname)

def test_debug_mode():
	path = os.path.abspath(__file__)
	dir_name = os.path.dirname(os.path.dirname(os.path.dirname(path)))
	libname = os.path.basename(dir_name)
	module = importlib.import_module(libname)
	assert module.DEBUG_MODE
