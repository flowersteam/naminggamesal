#!/usr/bin/python


from ngmeth import *
import my_functions
from scipy import optimize as sciopt
import random
import matplotlib.pyplot as plt
import multiprocessing
import custom_graph

MULTI_PROCESSING=1
NB_PROCESS=4

voctype="sparse"
M=2
W=2
nbagents=2
step=1

nb_iter=10
decoupage=20
Tmax=10000

j=0

#OPERATION=pop_ize(Nlink)
OPERATION=Nlinksurs



X=[]
for i in range(0,decoupage-1):
	X.append((i+1)/float(decoupage))

def function_to_optimize(param_array,**progressinfo):
	param=float(param_array)
	if param<=0 or param>=1:
		return ((param+1)*(param+1))**4*Tmax+2*Tmax
	strat={"strattype":"delaunaymodif"+str(param)}
	temppop=Population(voctype,strat,nbagents,M,W)
	for i in range(Tmax/step):
		if OPERATION(temppop)==M:#################################################
			return i/step
			break
		else:
			temppop.play_game(step)
			if "progress_info" in progressinfo.keys():
				progress_info=str(progressinfo["progress_info"])
			else:
				progress_info=""
			my_functions.print_on_line_pid(progress_info+" "+str(i*step)+"   "+str(param)+"     "+str(OPERATION(temppop)))




def compute(jj):
	Y=[]
	for i in range(len(X)):
		Y.append(function_to_optimize(np.array([X[i]]),progress_info=jj))
	return custom_graph.CustomGraph(X,Y,xmin=0,xmax=1)



# graph_list=[]
# if MULTI_PROCESSING and __name__=="__main__":
# 	proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
# 	graph_list=proc_pool.map_async(compute,range(0,nb_iter)).get(9999999)
# else:
# 	for j in range(0,10):
# 		graph_list.append(compute(j))



# tempgraph=graph_list[0]
# for j in range(0,nb_iter):
# 	tempgraph.add_graph(graph_list[j])

# tempgraph.std=1
# tempgraph.merge()
# tempgraph.show()

#raw_input("pressing enter will end program and close graphs")

#X1=np.array(range(1,10))*0.1







nb_iter_fun=10



def function_to_optimize_iteree(*args,**kwargs):
	Ytemp=[]
	if MULTI_PROCESSING and __name__=="__main__":
		proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
		Ytemp=proc_pool.map_async(function_to_optimize,range(0,nb_iter_fun)).get(9999999)
	else:
		for i in range(nb_iter_fun):
			Ytemp.append(function_to_optimize(*args,**kwargs))
	return np.mean(Ytemp)


	#x0=np.array([random.random()])

sol=[]
for i in range(0,100):
	solution=sciopt.minimize_scalar(function_to_optimize_iteree,bounds=[0.01,0.99],method='bounded')
	print solution.x
	sol.append(solution)

print "mean:"+str(np.mean(sol))+"    std:"+str(np.std(sol))

