import sys
from blessings import Terminal
from time import sleep
import multiprocessing


def print_on_line(txt,line_nb):
	term=Terminal()
	with term.location(0,line_nb):
		#with term.location(line_nb,0):
		#	print " "*term.width
		#print term.move(line_nb,0)+" "*term.width
		#with term.location(line_nb,0):
		print(txt+"                    ")
		#print term.move(line_nb,0)+txt
	print(term.move(term.height-2,0))
	#term.location()
	#print " ",

def get_worker_id():
	current_worker=multiprocessing.current_process()
	if len(current_worker._identity)==0:
		return 1
	else:
		return current_worker._identity[0]

def print_on_line_pid(txt):
	print_on_line(txt,get_worker_id()-1)

def params_list(PARAMS_DESCR):#NOT FINISHED
	tempdict={}
	nb_params=len(PARAMS_DESCR)
	multiplicity=[]
	nb_sets=1
	for i in range(0,nb_params):
		tempmult=len(params_list[1])
		multiplicity.append(tempmult)
		nb_sets=nb_sets*tempmult


