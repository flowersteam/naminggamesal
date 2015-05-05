#!/usr/bin/python


from ngmeth import *
import my_functions
from scipy import optimize as sciopt
import random
import matplotlib.pyplot as plt
import multiprocessing
import custom_graph
import copy
import cma

MULTI_PROCESSING=0
NB_PROCESS=2

voctype="sparse"
M=25
W=M
nbagents=M
step=1

nb_iter=5
Tmax=4000

j=0

#OPERATION=pop_ize(Nlink)
def OPERATION(pop):
	return 1-entropypop(pop)/entropypop_max(pop)



def function_to_optimize(param_array,**progressinfo):
	strat={"strattype":"decisionvector","decvec":param_array}
	temppop=Population(voctype,strat,nbagents,M,W)
	for i in range(len(param_array)):
		if not 0<=param_array[i]<=1:
			return (3+abs(param_array[i]))*Tmax
	for i in range(Tmax/step):
		value=OPERATION(temppop)
		if value==1.:#################################################
			return i/step
			break
		else:
			temppop.play_game(step)
			if "progress_info" in progressinfo.keys():
				progress_info=str(progressinfo["progress_info"])
			else:
				progress_info=""
			my_functions.print_on_line_pid(progress_info+" "+str(i*step)+"     "+str(value))
	return Tmax*(2-value)




# def compute(jj):
# 	Y=[]
# 	for i in range(len(X)):
# 		Y.append(function_to_optimize(np.array([X[i]]),progress_info=jj))
# 	return custom_graph.CustomGraph(X,Y,xmin=0,xmax=1)



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

# plot(  log2(W-m-1)*(m*m-m)   +log2(W-m)*(m*(1-M-W)-2*M*W)   +log2(W-m+1)*(-(M-m-1)*(W-m-1))    ,m=1..5),M=5,W=5





nb_iter_fun=5



def function_to_optimize_iteree(*args,**kwargs):
	Ytemp=[]
	int_ized=[]
	for i in range(len(args[0])):
		int_ized.append(int(args[0][i]))
	print int_ized
	print args[0]
	if MULTI_PROCESSING and __name__=="__main__":
		proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
		Ytemp=proc_pool.map_async(function_to_optimize,range(0,nb_iter_fun)).get(9999999)
	else:
		for i in range(nb_iter_fun):
			Ytemp.append(function_to_optimize(*args,**kwargs))
	return np.mean(Ytemp)


	#x0=np.array([random.random()])

def self_reference(f):
	f.func_defaults = f.func_defaults[:-1] + (f,)
	return f

@self_reference
def take_step(decv,self=None):
	decv_out=copy.deepcopy(decv)
	for i in range(-1,min(int(self.stepsize),len(decv_out)-2)):
		j=random.randint(1,len(decv_out)-2)
		decv_out[j]=1-decv_out[j]
	return decv_out

take_step.stepsize=M

# def accept_test(xnew=None):
# 	st=xnew[0]==1
# 	for i in range(1,len(xnew)):
# 		st=st and (xnew[i] in [0,1])
# 	st=st and xnew[-1]==0
# 	return st


decv0=np.ones(M+1)
decv0[-1]=0
for i in range(1,len(decv0)-1):
#	decv0[i]=random.randint(0,1)
	decv0[i]=0.5

solution=cma.fmin(function_to_optimize_iteree,decv0,0.1,noise_handler=cma.NoiseHandler(10))
# solution=sciopt.basinhopping(function_to_optimize_iteree, decv0, niter=10, T=Tmax, stepsize=0.5,  interval=10,disp=True)
print solution
print solution.x
# sol=[]
# for i in range(0,10):
	

# 	#solution=sciopt.basinhopping(function_to_optimize_iteree, decv0, niter=10, T=10000.0, stepsize=M, minimizer_kwargs=None, take_step=take_step, accept_test=accept_test, callback=None, interval=50, disp=False, niter_success=None)
# 	solution=sciopt.basinhopping(function_to_optimize_iteree, decv0, niter=10, T=Tmax, stepsize=0.5,  interval=10,disp=True)
	
	


# 	print "solution:"+str(solution.x)
# 	sol.append(solution)

# print sol