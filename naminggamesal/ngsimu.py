#!/usr/bin/python

import time
import uuid
import sqlite3
import os
import copy

try:
	import gexf
except ImportError:
	pass#version of pygexf on pip is not compatible with py3, possible to git clone the orig repo

from copy import deepcopy
try:
	import cPickle as pickle
except ImportError:
	import pickle

from .ngpop import Population
from . import ngmeth
from .tools import custom_func
from .tools import custom_graph
from .tools.sqlite_storage import SQLiteStorage,PostgresStorage,xz_compress,xz_decompress

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

import subprocess

class Poplist(object):
	def __init__(self,path,no_compressed_file=False,db_type='sqlite',conn_info=None,db_id=None):
		self.filepath = path
		if db_id is None:
			self.db_id = 'NG_'+str(uuid.uuid1())#''.join(str(uuid.uuid1()).split('-'))
		else:
			self.db_id = 'NG_'+db_id#''.join(db_id.split('-'))
		#if os.path.isfile(self.filepath+'.xz') and os.path.isfile(self.filepath): # Old Policy: if both compressed and uncompressed versions present, erase uncompressed
			#os.remove(self.filepath)
		self.pop = None
		#self.init_db()
		self.init_done = False
		#self.conn = sqlite3.connect(self.filepath)
		#self.cursor = self.conn.cursor()
		self.no_compressed_file = no_compressed_file
		if db_type == 'sqlite':
			self.storage = SQLiteStorage(filepath=path)
		elif db_type == 'postgres':
			self.storage = PostgresStorage(db_id=self.db_id,conn_info=conn_info)
		else:
			raise ValueError('db_type '+str(db_type)+' not recognized.')

	def clean_all(self):
		self.storage.clean_all()

	def init_db(self):
		self.storage.init_db()
		self.init_done = True

	def append(self,pop,T,no_storage=False):
		if hasattr(self,'init_done') and not self.init_done:
			self.init_db()
		if not no_storage:
			self.storage.add_data(data=pop,label=T)
		self.pop = pop
		self.T_last = T
		#add_data_conn(cursor=self.cursor,data=pop,label=T)

	def store_last(self):
		if hasattr(self,'init_done') and not self.init_done:
			self.init_db()
		if self.pop is None:
			self.pop = self.storage.read_data()
		self.storage.add_data(data=self.pop,label=self.T_last)

	def get(self,T):
		if hasattr(self,'T_last') and T == self.T_last:
			return self.get_last()
		else:
			return self.storage.read_data(label=T)
		#return read_data_conn(cursor=self.cursor,label=T)

	def get_last(self):
		if self.pop is None:
			self.pop = self.storage.read_data()
			#self.pop = read_data_conn(cursor=self.cursor)
		assert self.pop is not None
		return self.pop

	def compress(self,rm=True):
		#self.conn.commit()
		if os.path.exists(self.filepath) and not self.no_compressed_file:
			xz_compress(self.filepath,rm=rm)

	def __getstate__(self):
		#self.conn.commit()
		out_dict = self.__dict__.copy()
		out_dict['pop'] = None
		#del out_dict['conn']
		#del out_dict['cursor']
		return out_dict

	def __setstate__(self,in_dict):
		self.__dict__.update(in_dict)
		if os.path.isfile(self.filepath+'.xz') and os.path.isfile(self.filepath): # Policy: if both compressed and uncompressed versions present, erase uncompressed
			os.remove(self.filepath)
		#self.conn = sqlite3.connect(self.filepath)
		#self.cursor = self.conn.cursor()

class Experiment(object):

	def __init__(self, pop_cfg={}, step=1, no_storage=False, no_compressed_file=False, db_type='sqlite',conn_info=None):
		self._time_step = step
		self.define_stepfun()
		self._T = []
		self._exec_time=[]
		self.uuid = str(uuid.uuid1())
		self._pop_cfg = copy.deepcopy(pop_cfg)
		#self._pop_cfg['xp_uuid'] = self.uuid
		self._poplist = Poplist('data/' + self.uuid + '.db',no_compressed_file=no_compressed_file,db_type=db_type,conn_info=conn_info,db_id=self.uuid)
		#self.add_pop(Population(**pop_cfg),0)
		self.init_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.modif_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.reconstruct_info = []
		self.no_storage = no_storage

	def save_pop(self):
		self.init_poplist()
		pop = self._poplist.get_last()
		self._poplist.append(pop,self._T[-1])
		self.commit_to_db()

	def add_agent(self,agent):
		self.init_poplist()
		pop = self._poplist.get_last()
		pop.add_agent(agent)
		self._poplist.append(pop,self._T[-1])
		self.commit_to_db()

	def rm_agent(self,agent):
		self.init_poplist()
		pop = self._poplist.get_last()
		pop.rm_agent(agent)
		self._poplist.append(pop,self._T[-1])
		self.commit_to_db()

	def get_agent(self, agent_uuid):
		self.init_poplist()
		pop = self._poplist.get_last()
		agent_list = [ag for ag in pop._agentlist if ag._id == agent_uuid]
		if len(agent_list) == 0:
			raise KeyError('No agent with this uuid')
		else:
			return agent_list[0]

	def compress(self,rm=True):
		self._poplist.compress(rm=rm)

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
		if 'tempgraph' in list(out_dict.keys()):
			del(out_dict['tempgraph'])
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


	def init_poplist(self):
		if not self._T:
			self.add_pop(Population(xp_uuid=self.uuid,**self._pop_cfg),0,force_storage=True)


	#def __str__(self):
	#	return "T: "+str(self._T[-1])+"\n"+str(self._poplist.get_last())

	def continue_exp_until(self,T,monitoring_func=None):
		self.init_poplist()
		temptmax = self._T[-1]
		if monitoring_func is not None:
			monitoring_func(self)
		start_time = time.clock() - self._exec_time[-1]
		while (temptmax + self.stepfun(temptmax) <= T) :
			temppop = self._poplist.get_last()
			for tt in range(0,self.stepfun(temptmax)):
				temppop.play_game(1)
				self.reconstruct_info.append(temppop._lastgameinfo)
				self.reconstruct_info = self.reconstruct_info[-100:]
			end_time = time.clock()
			exec_time = end_time-start_time
			temppop._exec_time = exec_time
			self.add_pop(temppop,temptmax+self.stepfun(temptmax),exec_time=exec_time)
			temptmax += self.stepfun(temptmax)
			self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
			start_mon = time.clock()
			if monitoring_func is not None:
				monitoring_func(self)
			start_time += time.clock() - start_mon
			#self._T.append(temptmax)
			#self._exec_time.append(exec_time)

	def continue_exp(self,dT=None,monitoring_func=None):
		self.init_poplist()
		if dT is None:
			dT = self.stepfun(self._T[-1])
		self.continue_exp_until(self._T[-1]+dT,monitoring_func=monitoring_func)

	def add_pop(self,pop,T,exec_time=0,force_storage=False):
		pop._exec_time = exec_time
		if (not hasattr(self,'no_storage')) or (not self.no_storage) or force_storage:
			self._poplist.append(pop,T)
		else:
			self._poplist.append(pop,T,no_storage=True)
			#self._poplist.T_last = T
		self._T.append(T)
		self._exec_time.append(exec_time)

	def store_lastpop(self):
		self._poplist.store_last()

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
		if self.no_storage:
			if len(self._T)>2:
				tmin = self._T[-2]+0.1
			elif len(self._T) == 2:
				tmin = 0.1
			else:
				tmin = 0
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
		tempoutmean = []
		tempoutstd = []
		tempoutmin = []
		tempoutmax = []
		tempoutalldata = []
		if tempfun.level in ["agent","meaning"]:
			for j in range(indmin,len(self._T)+1+indmax):
				if hasattr(self,'no_storage') and self.no_storage:
					assert self._poplist.T_last == self._T[j] , str(self._poplist.T_last)+','+str( self._T[j])+','+str(tmin)
					tempout = copy.deepcopy(tempfun.apply(self._poplist.get_last()))
				else:
					tempout = copy.deepcopy(tempfun.apply(self._poplist.get(self._T[j])))
				tempoutmean.append(tempout[0])
				tempoutstd.append(tempout[1])
				tempoutmin.append(tempout[2])
				tempoutmax.append(tempout[3])
				tempoutalldata.append(tempout[4])
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempoutmean
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			stdvec=tempoutstd
			minvec=tempoutmin
			maxvec=tempoutmax
			all_datavec=tempoutalldata
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=1,sort=0,all_data=all_datavec,minvec=minvec,maxvec=maxvec,stdvec=stdvec,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="population":
			tempout=[]
			for j in range(indmin,len(self._T)+1+indmax):
				if hasattr(self,'no_storage') and self.no_storage:
					assert self._poplist.T_last == self._T[j] , str(self._poplist.T_last)+','+str( self._T[j])
					tempout.append(copy.deepcopy(tempfun.apply(self._poplist.get_last())))
				else:
					tempout.append(copy.deepcopy(tempfun.apply(self._poplist.get(self._T[j]))))
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempout
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="time":
			tempout = copy.deepcopy(tempfun.apply(self))
			tempout=tempout[indmin:(len(self._T)+indmax+1)]
			configgraph=tempfun.get_graph_config()
			configgraph["xlabel"]="T"
			tempY=tempout
			tempX=self._T[indmin:(len(self._T)+indmax+1)]
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		elif tempfun.level=="exp":
			tempout = copy.deepcopy(tempfun.apply(self))#,X=X)# TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			configgraph=tempfun.get_graph_config()
			#configgraph["xlabel"]="T"
			tempY=tempout
			tempX=[self._T[-1]]# TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			#configgraph["xmin"]=min(tempX)
			#configgraph["xmax"]=max(tempX)
			tempgraph=custom_graph.CustomGraph(X=tempX,Y=tempY,std=0,sort=0,filename="graph_"+tempfun.func.__name__,**configgraph)
		else:
			raise ValueError("Custom_func level doesn't exist or has an unknown value:"+str(tempfun.level))
		if X:
			tempgraph2=self.graph(method=X,tmin=tmin,tmax=tmax)
			tempgraph=tempgraph.func_of(tempgraph2)
		return tempgraph

	def old_animate(self,animation_type=None):#not working
		fig = plt.figure()
		def anim_func(i):
			t = self._T[i]
			pop = self._poplist.get(T=t)
			plt.clf()
			return pop.draw()#fig=fig, draw_type=animation_type)
		ani = animation.FuncAnimation(fig, anim_func, blit=False, interval=500, repeat=False, frames=len(self._T))#, init_func=init)
		return ani


	def second_animate(self,animation_type=None):
		filenames = []
		for t in self._T:
			pop = self._poplist.get(T=t)
			plt.clf()
			pop.draw()
			num = str(t)
			plt.savefig('image'+num+'.png', format='png')
			filenames.append('image'+num+'.png')
		from scitools.std import movie
		movie('*.png',fps=1,output_file='thisismygif.gif')
		#subprocess.call('ffmpeg -f image2 -r 10 -i image%07d.png -vcodec mpeg4 -y movie.mp4')



	def export_graph(self,filename=None):
		pop = self._poplist.get(T=0)
		gexf_elt = gexf.Gexf('William Schueller','Naming Games AL')
		G = gexf_elt.addGraph('undirected','dynamic','meaning space exploration')

		def color_of_node(pop,m):
			nag = 0
			for ag in pop._agentlist:
				if m in ag._vocabulary.get_known_meanings():
					nag += 1
				ag._vocabulary.del_cache()
			val = nag/float(len(pop._agentlist))
			if val == 0:
				return (1,0,0)
			elif val == 1.:
				return (0,1,0)
			else:
				return (1-val,1-val,1)

		def transform_color(col_val):
			if col_val == 0:
				return 0
			elif col_val == 1.:
				return 1
			elif 0 < col_val < 1.:
				return 0.5 + col_val*0.3

		pop = self._poplist.get(T=0)
		mG = pop.env.meaning_graph
		node_list = mG.nodes()
		edge_list = mG.edges()
		for m in node_list:
			G.addNode(m,m)
		e_id = 0
		for e in edge_list:
			G.addEdge(e_id,*e)
			e_id += 1
		id_col = G.addNodeAttribute('node_color','',mode='dynamic',type='string',force_id='color')
		id_col2 = G.addNodeAttribute('colorfloat','',mode='dynamic',type='float')
		id_col3 = G.addNodeAttribute('4color','',mode='dynamic',type='float')
		id_col4 = G.addNodeAttribute('srtheo','',mode='dynamic',type='float')
		for t_index in range(len(self._T)-1):
			t = self._T[t_index+1]
			t_m = self._T[t_index]
			lt = np.log(self._T[t_index+1])
			lt_m = np.log(self._T[t_index])
			pop = self._poplist.get(T=t)
			t1 = t_m
			t2 = t
			for m in node_list:
				col = color_of_node(pop,m)
				colsrtheo = ngmeth.srtheo(pop=pop,m=m)
				color = str(colors.rgb2hex(col))
				#color = str(col)
				#color = str(col[0])
				G._nodes[m].addAttribute(id=id_col,value=color)#,start=str(float(t_m)),end=str(float(t)))
				G._nodes[m].addAttribute(id=id_col2,value=str(1-col[0]),start=str(float(t1)),end=str(float(t2)))
				G._nodes[m].addAttribute(id=id_col3,value=str(transform_color(1-col[0])),start=str(float(t1)),end=str(float(t2)))
				G._nodes[m].addAttribute(id=id_col4,value=str(colsrtheo),start=str(float(t1)),end=str(float(t2)))
		if filename is None:
			filename = str(uuid.uuid1())
		if len(filename)<5 or filename[-5:]!='.gexf':
			filename = filename + '.gexf'
		with open(filename,"w") as output_file:
			output_file.write("<?xml version='1.0' encoding='utf-8'?>\n")
			gexf_elt.write(output_file)

