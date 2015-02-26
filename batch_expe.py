#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngmeth import *
import tmsu
import pickle
import time
import os
import multiprocessing

MULTI_PROCESSING=1
NB_PROCESS=4


PROGRESS_SHOW=1

if PROGRESS_SHOW:
	os.system("clear")


voctype="sparse"
PATH="./premiertest/"
tmsu_db="./premiertest/.tmsu/db"
tmsu_ng=tmsu.Tmsu(dbpath=tmsu_db,path=PATH)


egal=1

nb_iterations=1
stratlist=["naive"]
Mlist=[3]
Wlist=[10]
Nlist=[30,50,70]

nb_T=100
T=2000
T_step=max(T/nb_T,1)

param_set_list=[]
for iterr in range(0,nb_iterations):
	for strattype in stratlist:
		for M in Mlist:
			for W in Wlist:
				for N in Nlist:
					param_set_list.append([iterr,strattype,M,W,N])

def compute_batch(args_compute_batch):
	iterr=args_compute_batch[0]
	strattype=args_compute_batch[1]
	M=args_compute_batch[2]
	W=args_compute_batch[3]
	N=args_compute_batch[4]
	time_compact=time.strftime("%Y%m%d%H%M%S", time.localtime())
	filename="strat_"+strattype+"_M"+str(M)+"_W"+str(W)+"_"+str(N)+"agents_"+time_compact
	tempexp=Experiment(voctype,strattype,M,W,N,T_step)
	if PROGRESS_SHOW:
		tempexp.continue_exp(T,progress_info="iteration:"+str(iterr)+"/"+str(nb_iterations)+" "+filename)
	else:
		tempexp.continue_exp(T)
	if not os.path.exists(PATH+filename+".b") :
		temptags=[]
		tempexp.save(PATH+filename+".b")
		if egal==1:
			egal_or_not="="
		else:
			egal_or_not=""
		temptags.append("strategy"+egal_or_not+strattype)
		temptags.append("vocabulary"+egal_or_not+voctype)
		temptags.append("M"+egal_or_not+str(M))
		temptags.append("W"+egal_or_not+str(W))
		temptags.append("nbagents"+egal_or_not+str(N))
		temptags.append("Tmax"+egal_or_not+str(T))
		temptags.append("T_step"+egal_or_not+str(T_step))
		temptags.append("date"+egal_or_not+time_compact)
		temptags.append("filetype"+egal_or_not+"expebinary")
		tmsu_ng.tag(filename=PATH+filename+".b",tags=temptags)
	else:	
		print "filename déjà utilisé"

if MULTI_PROCESSING and __name__=="__main__":
	proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
	proc_pool.map_async(compute_batch,param_set_list).get(9999999)
else:
	for paramset in param_set_list:
		compute_batch(paramset)