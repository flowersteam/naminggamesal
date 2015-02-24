#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngmeth import *
import tmsu
import pickle
import custom_graph
import glob
import os

SHOW=1
PROGRESS_SHOW=0

TAG_BIN_EXPE="filetypebinaryexpe"
TAG_GRAPH_PREF=""

OUT_PATH="./premiertest/"
SOURCE_PATH="./premiertest/"
tmsu_db="./premiertest/.tmsu/db"
tmsu_ng=tmsu.Tmsu(dbpath=tmsu_db)
funclistpop=[Nlinkmoyenpop]
funclistexpe=[Nlinkmoyenexpe]

filelist=glob.glob(SOURCE_PATH+"strat*.b")
tempdataexpe=[]

for tempfunexpe in funclistexpe:
	for path_filename_num_ext in filelist:
		path_filename_ext=os.popen("readlink -f "+path_filename_num_ext, "r").read()
		filename_ext=os.path.basename(path_filename_ext)[:-1]
		filename=filename_ext[:-2]
		tempsimu=load_experiment(SOURCE_PATH+filename_ext)

		for tempfunpop in funclistpop:
			tempoutmean=[]
			tempoutstd=[]
			for j in range(0,len(tempsimu._poplist)):
				progress_info=tempfunexpe.__name__+" "+filename_ext+" "+tempfunpop.__name__+" T:"+str(tempsimu._T[j])+"/"+str(tempsimu._T[-1])
				if PROGRESS_SHOW:
					tempout=tempfunpop(tempsimu._poplist[j],progress_info)
				else:
					tempout=tempfunpop(tempsimu._poplist[j])
				tempoutmean.append(tempout[0])
				tempoutstd.append(tempout[1])
			configgraph={"xlabel":"Temps","ylabel":"Liens", "title":"Nombre moyen de liens par agent"}
			X=tempoutmean
			Y=tempsimu._T
			tempgraph=custom_graph.CustomGraph(X,Y,**configgraph)
			tempgraph.write_files()
			temptags=tmsu_ng.get_tags_list(filename=path_filename_ext)
			if TAG_BIN_EXPE in temptags:
				temptags.remove(TAG_BIN_EXPE)
			else:
				print "note: le tag_bin_expe n est pas dans les temptags"
			graphfilelist=[tempgraph.filename+".b"]
			tmsu_ng.tag(filename=filename+".b",tags="binarygraph")
			tmsu_ng.tag(filename=filename+".b",tags=temptags)
			for extension in tempgraph.extensions:
				graphfilelist.append(tempgraph.filename+"."+extension)
				tmsu_ng.tag(filename=filename+"."+extension,tags=extension)
				tmsu_ng.tag(filename=filename+"."+extension,tags=temptags)
			if SHOW:
				tempgraph.show()

			tempout=tempfunexpe(tempsimu)
			tempdataexpe.append(tempout)

# for tempfunexpe in funclistexpe:
# 	%%config graph
# 	%%tempgraph=custom_graph.CustomGraph(X,Y,**kwargs)
# 	tempgraph.write_files()
# 	temptags=tmsu_ng.get_tags_list(filename=path_filename_num_ext)
# 	temptags.remove(TAG_BIN_EXPE)
# 	graphfilelist=[tempgraph.filename+".b"]
# 	tmsu_ng.tag(filename=filename+".b",tags="binarygraph")
# 	tmsu_ng.tag(filename=filename+".b",tags=temptags)
# 	for extension in tempgraph.extensions:
# 		graphfilelist.append(tempgraph.filename+"."+extension)
# 		tmsu_ng.tag(filename=filename+"."+extension,tags=extension)
# 		tmsu_ng.tag(filename=filename+"."+extension,tags=temptags)
# if SHOW:
# 	tempgraph.show()
