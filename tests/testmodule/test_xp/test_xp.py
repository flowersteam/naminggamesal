import pytest
import copy
import random
import numpy as np
import os

import tempfile
import naminggamesal as ngal
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
	'lapsmax_mab_explothreshold',
	]
@pytest.fixture(params=strat_list)
def strattype(request):
	return request.param

simple_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':'matrix_new'},
        'strat_cfg':{'strat_type':'naive',
                    'vu_cfg':{'vu_type':'minimal'},
                    'success_cfg':{'success_type':'global_norandom'}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':'log_improved'
    }

#@pytest.mark.parametrize("voctype", voctype_list)
#@pytest.mark.parametrize("vutype", vutype_list)
#@pytest.mark.parametrize("steptype", steptype_list)
@pytest.fixture
def xp_cfg_struct(voctype,steptype):
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':voctype},
        'strat_cfg':{'strat_type':'naive',
                    'vu_cfg':{'vu_type':'minimal'},
                    'success_cfg':{'success_type':'global_norandom'}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':steptype
    }
	return base_xp_cfg

@pytest.fixture
def xp_cfg(vutype,successtype,strattype):
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':'matrix_new'},
        'strat_cfg':{'strat_type':strattype,
                    'vu_cfg':{'vu_type':vutype},
                    'success_cfg':{'success_type':successtype}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':'log_improved'
    }
	return base_xp_cfg

@pytest.fixture
def xp_cfg2(successtype,strattype):
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':'matrix_new'},
        'strat_cfg':{'strat_type':strattype,
                    'vu_cfg':{'vu_type':'minimal'},
                    'allow_idk':True,
                    'success_cfg':{'success_type':successtype}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':'log_improved'
    }
	return base_xp_cfg

local_m_list = ['srtheo',
				'Nlink',
				'N_d',
				'N_meanings',
				'N_words',
				'homonymy',
				'synonymy',
				'exec_time']

# extended_local_m_list = [
# 				'N_d',
# 				'exec_time'] + local_m_list

extended_local_m_list = ngal.get_allfunc(level='agent') + ngal.get_allfunc(level='population')
@pytest.fixture(params=extended_local_m_list)
def local_m(request):
	return request.param

global_m_list = ['conv_time',
				'conv_time2',
				'max_mem',
				'max_N_d',
				'max_N_d_time',
				'max_Nlink_time',
				'tdiff_d',
				'tdiff_w',
				'tdiff_wd',
				]

# extended_global_m_list = ['conv_time',
# 				'conv_time2',
# 				] + global_m_list

extended_global_m_list = ngal.get_allfunc(level='exp')
@pytest.fixture(params=extended_global_m_list)
def global_m(request):
	return request.param


def xp_loop(cfg):
	xp = db.get_experiment(**cfg)
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

def test_struct(xp_cfg_struct):
	xp_loop(xp_cfg_struct)


def test_xp(xp_cfg):
	xp_loop(xp_cfg)

def test_xp_allowidk(xp_cfg2):
	xp_loop(xp_cfg2)

def test_localm(local_m):
	xp = db.get_experiment(**simple_cfg)
	xp.continue_exp_until(40)
	xp.graph(local_m)


def test_globalm(global_m):
	xp = db.get_experiment(**simple_cfg)
	xp.continue_exp_until(40)
	xp.graph(global_m)


######### AGENT INIT ###############
agentinit_list = [
	'converged',
	'own_words',
	]
@pytest.fixture(params=agentinit_list)
def agentinittype(request):
	return request.param

def test_agentinit(agentinittype):
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':'matrix_new'},
        'agent_init_cfg':{'agent_init_type':agentinittype},
        'strat_cfg':{'strat_type':'naive',
                    'vu_cfg':{'vu_type':'minimal'},
                    'success_cfg':{'success_type':'global_norandom'}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':'log_improved'
    }
	xp_loop(base_xp_cfg)


######### BROADCASTING ###############

def test_braodcasting():
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':'matrix_new'},
        'strat_cfg':{'strat_type':'naive',
                    'vu_cfg':{'vu_type':'minimal','broadcasting':True},
                    'success_cfg':{'success_type':'global_norandom'}},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':'log_improved'
    }
	xp_loop(base_xp_cfg)


######### WORD PREFERENCE ###############
wordpreference_list = [
	'wordpreference_last',
	'wordpreference_first',
	'wordpreference_smart',
	]
@pytest.fixture(params=wordpreference_list)
def wordpreferencetype(request):
	return request.param

def test_wordpreference(wordpreferencetype):
	base_xp_cfg = {
    'pop_cfg':{
        'voc_cfg':{'voc_type':'matrix_new'},
        'strat_cfg':{'strat_type':'naive',
                    'vu_cfg':{'vu_type':'minimal'},
                    'success_cfg':{'success_type':'global_norandom'},
                    'memory_policies':[{'mem_type':wordpreferencetype}]},
        'interact_cfg':{'interact_type':'speakerschoice'},
        'env_cfg':{'env_type':'simple','M':M,'W':W},
        'nbagent':N
    },
    'step':'log_improved'
    }
	xp_loop(base_xp_cfg)

