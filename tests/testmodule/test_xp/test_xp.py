import pytest
import copy
import random
import numpy as np
import os

import tempfile
from naminggamesal import ngvoc,ngmeth,ngdb

newpath = tempfile.mkdtemp()
os.chdir(newpath)

db = ngdb.NamingGamesDB('pytest_db.db')


M = 10
W = 10
N = 10

voctype_list = [
	'2dictdict',
	'matrix_new',
	'sparse_new',
	]
@pytest.fixture(params=voctype_list)
def voctype(request):
	return request.param

vutype_list = [
	'minimal',
	'imitation',
	'BLIS',
	]
@pytest.fixture(params=vutype_list)
def vutype(request):
	return request.param

steptype_list = [
	'log_improved',
	5,
	]
@pytest.fixture(params=steptype_list)
def steptype(request):
	return request.param

success_list = [
	'global',
	'global_norandom',
	'alignment',
	'communicative'
	]
@pytest.fixture(params=success_list)
def successtype(request):
	return request.param

strat_list = [
	'naive',
	'success_threshold',
	'success_threshold_wise',
	'lapsmax_explothreshold',
	]
@pytest.fixture(params=strat_list)
def strattype(request):
	return request.param


#@pytest.mark.parametrize("voctype", voctype_list)
#@pytest.mark.parametrize("vutype", vutype_list)
#@pytest.mark.parametrize("steptype", steptype_list)
@pytest.fixture
def xp_cfg(voctype,vutype,steptype,successtype,strattype):
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':voctype},
        'strat_cfg':{'strat_type':strattype,
                    'vu_cfg':{'vu_type':vutype},
                    'success_cfg':{'success_type':successtype}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':steptype
    }
	return base_xp_cfg

local_m_list = ['srtheo',
				'Nlink',
				'N_d',
				'homonymy',
				'synonymy',
				'exec_time']


global_m_list = ['conv_time',
				'max_mem',
				'max_N_d',
				]

def test_xp(xp_cfg):
	xp = db.get_experiment(**xp_cfg)
	xp.continue_exp_until(20)
	for local_m in local_m_list:
		xp.graph(local_m)
	for global_m in global_m_list:
		xp.graph(global_m)
	xp.continue_exp_until(40)
	for local_m in local_m_list:
		xp.graph(local_m)
	for global_m in global_m_list:
		p = xp.graph(global_m)
		assert len(p._X) == 1 and len(p._X[0]) == 1

