#!/usr/bin/python
# -*- coding: latin-1 -*-

import lib.ngdb as ngdb
import multiprocessing
import my_functions


MULTIPROCESS=1
NB_PROCESS=3

PROGRESS_SHOW=0

#DB_PATH="naminggames.db"


iterr=3
T_max=100
T_step=1+int(T_max/100)

PARAMS_DESCR=[
	["voctype",["sparse"]],
	["strat",[{"strattype":"naive"},
		{"strattype":"delaunay"},
		{"strattype":"naivereal"}]],
	["nb_ag",[10]],
	["M",[5,10]],
	["W",[10]],
	["step",[T_step]]
	]


PARAMS_LIST=additional.my_functions.params_list(PARAMS_DESCR)

def compute_batch(**params):
	tempexp=ngdb.Experiment(**params)
	if PROGRESS_SHOW:
		tempexp.continue_exp_until(T_max,progress_info="test")
	else:
		tempexp.continue_exp_until(T_max)


if MULTI_PROCESSING and __name__=="__main__":
	proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
	proc_pool.map_async(compute_batch,PARAMS_LIST).get(9999999)
else:
	for paramset in PARAMS_LIST:
		compute_batch(paramset)