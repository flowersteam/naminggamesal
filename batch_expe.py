#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngmeth import *
import tmsu
import pickle
import time
import os

voctype="sparse"
PATH="./premiertest/"
tmsu_db="./premiertest/.tmsu/db"
tmsu_ng=tmsu.Tmsu(dbpath=tmsu_db,path=PATH)


egal=0

nb_iterations=1
stratlist=["naive"]
Mlist=[3]
Wlist=[3]
Nlist=[3,5,7]

nb_T=100
T=2000
T_step=T/nb_T


for iterr in range(0,nb_iterations):
	for strattype in stratlist:
		for M in Mlist:
			for W in Wlist:
				for N in Nlist:

					time_compact=time.strftime("%Y%m%d%H%M%S", time.localtime())
					filename="strat_"+strattype+"_M"+str(M)+"_W"+str(W)+"_"+str(N)+"agents_"+time_compact
					tempexp=Experiment(voctype,strattype,M,W,N,T_step)
					tempexp.continue_exp(T,"iteration:"+str(iterr)+"/"+str(nb_iterations)+" "+filename)
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
