#!/usr/bin/python

import time
import uuid
import sqlite3

from copy import deepcopy
import cPickle

from .ngpop import Population
from . import ngmeth
import additional.custom_func as custom_func
import additional.custom_graph as custom_graph
from additional.sqlite_storage import add_data,read_data,xz_compress,xz_decompress



class Poplist(object):
	def __init__(self,path):
		self.filepath = path
		self.pop = None
		#self.conn = sqlite3.connect(self.filepath)
		#self.cursor = self.conn.cursor()

	def append(self,pop,T):
		add_data(filepath=self.filepath,data=pop,label=T)
		#add_data_conn(cursor=self.cursor,data=pop,label=T)

	def get(self,T):
		return read_data(filepath=self.filepath,label=T)
		#return read_data_conn(cursor=self.cursor,label=T)

	def get_last(self):
		if self.pop is None:
			self.pop = read_data(filepath=self.filepath)
			#self.pop = read_data_conn(cursor=self.cursor)
		return self.pop

	def compress(self):
		#self.conn.commit()
		xz_compress(self.filepath,rm=True)

	def __getstate__(self):
		#self.conn.commit()
		out_dict = self.__dict__.copy()
		out_dict['pop'] = None
		#del out_dict['conn']
		#del out_dict['cursor']
		return out_dict

	def __setstate__(self,in_dict):
		self.__dict__.update(in_dict)
		#self.conn = sqlite3.connect(self.filepath)
		#self.cursor = self.conn.cursor()



class Experiment(object):

	def __init__(self, pop_cfg, step=1):
		self._time_step = step
		self.define_stepfun()
		self._T = []
		self._exec_time=[]
		self._pop_cfg = pop_cfg
		self.uuid = str(uuid.uuid1())
		self._poplist = Poplist('data/' + self.uuid + '.db')
		self.add_pop(Population(**pop_cfg),0)
		self.init_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.modif_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.reconstruct_info = []

	def compress(self):
		self._poplist.compress()

	def define_stepfun(self):
		if self._time_step == 'log':
			self.stepfun = self.logstepfun
		elif self._time_step == 'log_improved':
			self.stepfun = self.logstepfun2
		elif isinstance(self._time_step,int):
			self.stepfun = self.linearstepfun
		else:
			raise Exception('unknown step function definition: '+str(self._time_step))

	def __getstate__(self):
		out_dict = self.__dict__.copy()
		out_dict['stepfun'] = None
		return out_dict


	def __setstate__(self, in_dict):
		self.__dict__.update(in_dict)
		self.define_stepfun()

	def backwards_stepfun(self,time):
		i = 1
		while time - i + self.stepfun(time-i) > time:
			i += 1
			assert(time>=i)
		return i

	def logstepfun(self,time,backwards=False):
		time = int(time)
		if time <= 1:
			return 1
		oom = len(str(time))-1
		double_prefix = int((10*time)/(10**oom))
		if double_prefix < 15:
			out_prefix = 1.5
			backw_prefix = 0.7
		elif double_prefix < 20:
			out_prefix = 2.
			backw_prefix = 1.
		elif double_prefix < 30:
			out_prefix = 3.
			backw_prefix = 1.5
		elif double_prefix < 50:
			out_prefix = 5.
			backw_prefix = 2.
		elif double_prefix < 70:
			out_prefix = 7.
			backw_prefix = 3.
		else:
			out_prefix = 10.
			backw_prefix = 5.
		if backwards:
			return int(time - backw_prefix*(10**oom))
		else:
			return int(out_prefix*(10**oom)-time)

	def logstepfun2(self,time,backwards=False):
		time = int(time)
		if time <= 10:
			return 1
		oom = len(str(time))-1
		double_prefix = int((10*time)/(10**oom))
		if double_prefix == 10:
			step_out_prefix = 0.1
			step_backw_prefix = 0.05
		elif double_prefix <= 39:
			step_out_prefix = 0.1
			step_backw_prefix = 0.1
		elif double_prefix == 40:
			step_out_prefix = 0.2
			step_backw_prefix = 0.1
		elif double_prefix <= 69:
			step_out_prefix = 0.2
			step_backw_prefix = 0.2
		elif double_prefix == 70:
			step_out_prefix = 0.5
			step_backw_prefix = 0.2
		elif double_prefix <= 99:
			step_out_prefix = 0.5
			step_backw_prefix = 0.5
		if backwards:
			return int(step_backw_prefix*(10**oom))
		else:
			return int(step_out_prefix*(10**oom))

	def linearstepfun(self,time,backwards=False):
		return self._time_step



	def __str__(self):
		return "T: "+str(self._T[-1])+"\n"+str(self._poplist.get(self._T[-1]))

	def continue_exp_until(self,T):
		temptmax = self._T[-1]
		start_time = time.clock() - self._exec_time[-1]
		while (temptmax + self.stepfun(temptmax) <= T) :
			temppop = self._poplist.get_last()
			for tt in range(0,self.stepfun(temptmax)):
				temppop.play_game(1)
				self.reconstruct_info.append(temppop._lastgameinfo)
				self.reconstruct_info = self.reconstruct_info[-100:]
			end_time = time.clock()
			self.add_pop(temppop,temptmax+self.stepfun(temptmax),exec_time=end_time-start_time)
			temptmax += self.stepfun(temptmax)
			self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

	def continue_exp(self,dT=None):
		if dT is None:
			dT = self.stepfun(self._T[-1])
		self.continue_exp_until(self._T[-1]+dT)

	def add_pop(self,pop,T,exec_time=0):
		self._poplist.append(pop,T)
		self._T.append(T)
		self._exec_time.append(exec_time)

#	def set_time_step(self,newstep):
#		self._time_step=newstep

	def visual(self,vtype=None,ag_list=None,tmax=None):
		if tmax==None:
			tmax=self._T[-1]
		ind=-1
		while self._T[ind]>tmax:
			ind-=1
		self._poplist[ind].visual(vtype=vtype,ag_list=ag_list)

	def graph(self,method="srtheo",X=None,tmin=0,tmax=None):
		if not tmax:
			tmax = self._T[-1]
		indmax=-1
		if tmax >= self._T[-1] + self.stepfun(self._T[-1]):
			self.continue_exp_until(tmax)
			return self.graph(method=method, X=X, tmin=tmin, tmax=tmax)
		while self._T[indmax]>tmax:
			indmax-=1
		indmin=0
		while self._T[indmin]<tmin:
			indmin+=1
		tempfun=getattr(ngmeth,"custom_"+method)
		tempoutmean=[]
		tempoutstd=[]
		if tempfun.level=="agent":
			for j in range(indmin,len(self._T)+1+indmax):
				tempout=tempfun.apply(self._poplist.get(self._T[j]))
				tempoutmean.append(tempout[0])
				tempoutstd.append(tempout[1])
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempoutmean
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			stdvec=tempoutstd
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=1,sort=0,stdvec=stdvec,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="population":
			tempout=[]
			for j in range(indmin,len(self._T)+1+indmax):
				tempout.append(tempfun.apply(self._poplist.get(self._T[j])))
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempout
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="time":
			tempout=tempfun.apply(self)
			tempout=tempout[indmin:(len(self._T)+indmax+1)]
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempout
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="exp":
			tempout=tempfun.apply(self)#,X=X)# TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			configgraph=tempfun.get_graph_config()
			#configgraph["xlabel"]="T"
			tempY=tempout
			tempX=[self._T[-1]]# TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		else:
			print("Custom_func level doesn't exist or has an unknown value:")
			print(tempfun.level)
		if X:
			tempgraph2=self.graph(method=X,tmin=tmin,tmax=tmax)
			tempgraph=tempgraph.func_of(tempgraph2)
		return tempgraph



