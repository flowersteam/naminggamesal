#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngmeth import *
import tmsu
import pickle
import custom_graph
import glob
import os
import copy
import multiprocessing



#tmsu repair -D ./premiertest/.tmsu/db --remove
#tmsu mount -o allow_other -D ./premiertest/.tmsu/db /home/will/tmsufs
#
#
#
MULTI_PROCESSING=0
NB_PROCESS=1

SHOW_POP=0
SHOW_EXPE=1
KEEP_PLOTWIN_OPEN=0
PROGRESS_SHOW=1
if PROGRESS_SHOW:
	os.system("clear")

GRAPH_STD=1
GRAPH_MULTI=0

TAG_BIN_EXPE="filetype=expebinary"

OUT_PATH="./premiertest/"
SOURCE_PATH_LIST=["./premiertest/"]
tmsu_db="./premiertest/.tmsu/db"
tmsu_ng=tmsu.Tmsu(dbpath=tmsu_db)
funclist=[custom_Nlinksurs,custom_success_rate]




for SOURCE_PATH in SOURCE_PATH_LIST:
	
	filelist=glob.glob(SOURCE_PATH+"strat*.b")
	
	##GET Yopt/X values niveau expe en comparant les filenames
	filelist_parsed=[]
	for path_filename_num_ext in filelist:
		path_filename_ext=os.popen("readlink -f "+path_filename_num_ext, "r").read()
		filename_ext=os.path.basename(path_filename_ext)[:-1]
		filename=filename_ext[:-2]
		filename=filename.split('_')
		filename=filename[:-1]
		filelist_parsed.append(filename)
	
	cond=1
	model=filelist_parsed[0]
	for i in range(0,len(filelist_parsed[0])):
			for filename in filelist_parsed:
				if filename[i]!=model[i]:
					if cond:
						differing_param_indice=i
						cond=0
	
	XY=[]
	if differing_param_indice==1:
		differing_param="Stratégie"
		differing_param_id="strat"
		for filename in filelist_parsed:
			XY.append(filename[1])
	elif differing_param_indice==2:
		differing_param="Nombre total de meanings"
		differing_param_id="M"
		for filename in filelist_parsed:
			XY.append(int(filename[2][1:]))
	elif differing_param_indice==3:
		differing_param="Nombre total de words"
		differing_param_id="W"
		for filename in filelist_parsed:
			XY.append(int(filename[3][1:]))
	else:
		differing_param="Nombre d'agents"
		differing_param_id="N"
		for filename in filelist_parsed:
			XY.append(int(filename[4][:-6]))
	
	
	###BOUCLE PRINCIPALE

	def compute_batch(tempfun_nb):
		tempfun=funclist[tempfun_nb]
		tempdataexpe=[]
		for path_filename_num_ext in filelist:
			path_filename_ext=os.popen("readlink -f "+path_filename_num_ext, "r").read()
			filename_ext=os.path.basename(path_filename_ext)[:-1]
			filename=filename_ext[:-2]
			tempsimu=load_experiment(SOURCE_PATH+filename_ext)
			tempoutmean=[]
			tempoutstd=[]
	
	
			if tempfun.level=="agent":
				for j in range(0,len(tempsimu._poplist)):
					progress_info=tempfun.func.__name__+" "+filename_ext+" T:"+str(tempsimu._T[j])+"/"+str(tempsimu._T[-1])
					if PROGRESS_SHOW:
						tempout=tempfun.apply(tempsimu._poplist[j],progress_info=progress_info)
					else:
						tempout=tempfun.apply(tempsimu._poplist[j])
					tempoutmean.append(tempout[0])
					if GRAPH_STD:
						tempoutstd.append(tempout[1])
				configgraph=tempfun.get_graph_config()
				configgraph["xlabel"]="T"
				Y=tempoutmean
				X=tempsimu._T
				stdvec=tempoutstd
				tempgraph=custom_graph.CustomGraph(X,Y,std=GRAPH_STD,sort=0,stdvec=stdvec,filename="graph_"+tempfun.func.__name__+"_"+filename,**configgraph)
				if SHOW_POP:
					tempgraph.show()
				tempgraph.write_files(OUT_PATH)
				temptags=tmsu_ng.get_tags_list(filename=path_filename_ext)
				temptags.append("fonction="+tempfun.func.__name__)
				if TAG_BIN_EXPE in temptags:
					temptags.remove(TAG_BIN_EXPE)
				else:
					print "note: le tag_bin_expe n est pas dans les temptags"
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=["filetype=binarygraph"])
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=temptags)
				for extension in tempgraph.extensions:
					tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=["filetype="+extension])
					tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=temptags)
	
				tempdataexpe.append(copy.deepcopy(tempgraph))
	
	
			elif tempfun.level=="population":
				tempout=[]
				for j in range(0,len(tempsimu._poplist)):
					progress_info=tempfun.func.__name__+" "+filename_ext+" T:"+str(tempsimu._T[j])+"/"+str(tempsimu._T[-1])
					if PROGRESS_SHOW:
						tempout.append(tempfun.apply(tempsimu._poplist[j],progress_info=progress_info))
					else:
						tempout.append(tempfun.apply(tempsimu._poplist[j]))
				configgraph=tempfun.get_graph_config()
				Y=tempout
				X=tempsimu._T
				tempgraph=custom_graph.CustomGraph(X,Y,sort=0,filename="graph_"+tempfun.func.__name__+filename,**configgraph)
				if SHOW_POP:
					tempgraph.show()
				tempgraph.write_files(OUT_PATH)
				temptags=tmsu_ng.get_tags_list(filename=path_filename_ext)
				temptags.append("fonction="+tempfun.func.__name__)
				if TAG_BIN_EXPE in temptags:
					temptags.remove(TAG_BIN_EXPE)
				else:
					print "note: le tag_bin_expe n est pas dans les temptags"
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=["filetype=binarygraph"])
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=temptags)
				for extension in tempgraph.extensions:
					tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=["filetype="+extension])
					tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=temptags)
	
				tempdataexpe.append(copy.deepcopy(tempgraph))
	
	
			elif tempfun.level=="experiment":
	
				tempout=tempfun.apply(tempsimu)
				tempdataexpe.append(tempout)
	
		if tempfun.level=="agent" or "population":
			tempgraph=tempdataexpe[0]
			tempgraph.Yoptions[0]["label"]=differing_param_id+"="+str(XY[0])
			for i in range(1,len(tempdataexpe)):
				tempdataexpe[i].Yoptions[0]["label"]=differing_param_id+"="+str(XY[i])
				tempgraph.add_graph(tempdataexpe[i])
			timecompact=time.strftime("%Y%m%d%H%M%S", time.localtime())
			temp1="graph_"+tempfun.func.__name__+"_"+tempfun.level+"_"+differing_param_id+"_"
			temp2="_"+timecompact
			tempgraph.filename=temp1+"multi"+temp2
			tempgraph.title=temp1+"multi"+temp2
			tempgraph.std=0
			if SHOW_EXPE:
				tempgraph.show()
			tempgraph.write_files(OUT_PATH)
			#TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGS
			temptags=["level="+tempfun.level,"multi","diffparam="+differing_param_id,"date="+timecompact,"fonction="+tempfun.func.__name__,"strat="+filelist_parsed[0][1]]
			tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=["filetype=binarygraph"])
			tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=temptags)
			for extension in tempgraph.extensions:
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=["filetype="+extension])
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=temptags)
	
			tempgraph.filename=temp1+"merged"+temp2
			tempgraph.title=temp1+"merged"+temp2
			tempgraph.merge()
			tempgraph.std=1
			tempgraph.Yoptions=[{}]
			if SHOW_EXPE:
				tempgraph.show()
			tempgraph.write_files(OUT_PATH)
			#TAAAAAAAAAAAAAAAAAAAAAAAAAAAAGS
			temptags=["level="+tempfun.level,"merged","diffparam="+differing_param_id,"date="+timecompact,"fonction="+tempfun.func.__name__,"strat="+filelist_parsed[0][1]]
			tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=["filetype=binarygraph"])
			tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=temptags)
			for extension in tempgraph.extensions:
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=["filetype="+extension])
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=temptags)
	
		elif tempfun.level=="experiment":
			configgraph={"xlabel":differing_param}
			#Si plusieurs data pour la meme value du diff param, il faut encore implementer le tri/mean/std!!
			tempgraph=custom_graph.CustomGraph(XY,tempdataexpe,sort=1,**configgraph)
			temp1="graph_"+tempfun.func.__name__+"_"+tempfun.level+"_"+differing_param_id+"_"+time.strftime("%Y%m%d%H%M%S", time.localtime())
			tempgraph.filename=temp1
			tempgraph.std=0
			if SHOW_EXPE:
				tempgraph.show()
			tempgraph.write_files(OUT_PATH)
			#TAAAAAAAAAAAAAAAAAAAAAAAAAAAAGS
			temptags=["level="+tempfun.level,"diffparam="+differing_param_id,"date="+timecompact,"fonction="+tempfun.func.__name__,"strat="+filelist_parsed[0][1]]
			tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=["filetype=binarygraph"])
			tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+".b",tags=temptags)
			for extension in tempgraph.extensions:
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=["filetype="+extension])
				tmsu_ng.tag(filename=OUT_PATH+tempgraph.filename+"."+extension,tags=temptags)
	


###################### EXECUTION####################################

if MULTI_PROCESSING and __name__=="__main__":
	proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
	test=proc_pool.map_async(compute_batch,range(len(funclist))).get(9999999)
else:
	for tempfun_nb in range(len(funclist)):
		compute_batch(tempfun_nb)


#pausing to keep graphs opened
if (SHOW_EXPE or SHOW_POP) and KEEP_PLOTWIN_OPEN:
	raw_input("Press Enter to end program and close graphs")

#PYTHON3
#import msvcrt as m
# def wait():
#     m.getch()