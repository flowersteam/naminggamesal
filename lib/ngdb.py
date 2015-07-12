#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sqlite3 as sql
import time
import bz2
import cPickle
from copy import deepcopy

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph

from . import ngmeth
from . import ngsimu

class NamingGamesDB(object):
	def __init__(self,path=None):
		self.pickle_protocol=1
		if not path:
			path='naminggames.db'
		self.dbpath=path
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
				+"Id TEXT, "\
				+"Creation_Time INT, "\
				+"Modif_Time INT, "\
				+"PopConfig TEXT, "\
				+"Tmax INT, "\
				+"step INT, "\
				+"Experiment_object BLOB)")
			cursor.execute("CREATE TABLE IF NOT EXISTS computed_data_table("\
				+"Id TEXT, "\
				+"Creation_Time INT, "\
				+"Modif_Time INT, "\
				+"Function TEXT, "\
				+"Custom_Graph BLOB)")

	def merge(self,other_dbpath,remove=False,main_only=False):
		other_db=NamingGamesDB(other_dbpath)
		id_list=other_db.get_id_list(all_id=True)
		for nb_id in id_list:
			if self.id_in_db(nb_id) and (self.get_modif_time(nb_id)<other_db.get_modif_time(nb_id)):
				self.commit(other_db.get_experiment(nb_id=nb_id))
				#these few lines would be seen as repetitive and unnecessary, but for large databases it avoids loading all experiment objects, just the needed ones
			elif not self.id_in_db(nb_id):
				self.commit(other_db.get_experiment(nb_id=nb_id))
		if not main_only:
			for nb_id in id_list:
				other_methd_list=other_db.get_method_list(nb_id)
				methd_list=self.get_method_list(nb_id)
				for met in other_methd_list:
					if (met in methd_list) and (self.get_modif_time(nb_id,graph=met)<other_db.get_modif_time(nb_id,graph=met)):
						self.commit_data(other_db.get_experiment(nb_id=nb_id),other_db.get_graph(nb_id,method=met),met)
					elif not (met in methd_list):
						self.commit_data(other_db.get_experiment(nb_id=nb_id),other_db.get_graph(nb_id,method=met),met)
		if remove:
			os.remove(other_dbpath)

	def get_method_list(self,nb_id):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			cursor.execute("SELECT Function FROM computed_data_table WHERE Id=\'"+str(nb_id)+"\'")
			templist=list(cursor)
			for i in range(0,len(templist)):
				templist[i]=templist[i][0]
			return templist

	def get_modif_time(self,nb_id,graph=None):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			if not graph:
				cursor.execute("SELECT Modif_Time FROM main_table WHERE Id=\'"+str(nb_id)+"\'")
				return cursor.fetchone()[0]
			else:
				cursor.execute("SELECT Modif_Time FROM computed_data_table WHERE Id=\'"+str(nb_id)+"\' AND Function==\'"+graph+"\'")
				return cursor.fetchone()[0]

	def id_in_db(self,nb_id):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			cursor.execute("SELECT Id FROM main_table WHERE Id=\'"+str(nb_id)+"\'")
			if cursor.fetchall():
				return True
			else:
				return False

	def get_experiment(self,nb_id=None,force_new=False,blacklist=[],**params):
		if force_new:
			return Experiment(database=self,**params)
		if nb_id:
			if self.id_in_db(nb_id):
				conn=sql.connect(self.dbpath)
				with conn:
					cursor=conn.cursor()
					cursor.execute("SELECT Experiment_object FROM main_table WHERE Id=\'"+str(nb_id)+"\'")
					tempblob=cursor.fetchone()
					return cPickle.loads(bz2.decompress(str(tempblob[0])))
			else:
				print("ID doesn't exist in DB")
		else:
			templist=self.get_id_list(**params)
			for elt in blacklist:
				try:
					templist.remove(elt)
				except ValueError:
					pass
			if templist:
				i=random.randint(0,len(templist)-1)
				return self.get_experiment(nb_id=templist[i])
			else:
				return Experiment(database=self,**params)


	def get_graph(self,nb_id,method="srtheo"):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			cursor.execute("SELECT Custom_Graph FROM computed_data_table WHERE Id=\'"+str(nb_id)+"\' AND Function=\'"+method+"\'")
			tempblob=cursor.fetchone()
			return cPickle.loads(bz2.decompress(str(tempblob[0])))

	def get_condition_sql_format(self,**params):
		changedic={\
			"voctype":"Voctype",\
			"strat":"Strat",\
			"M":"M",\
			"W":"W",\
			"step":"step",\
			"nbagent":"Nb_agent",\
			}
		tempstr=""
		if "sql_condition" in params.keys():
			return params["sql_condition"]
		else:
			put_and=False
			for name, value in params.items():
				if put_and:
					tempstr+=" AND"
				if name=="strat":
					tempstr+=" "+changedic[name]+"=\'"+str(value["strattype"])+"\'"
				else:
					tempstr+=" "+changedic[name]+"=\'"+str(value)+"\'"
				put_and=True
			return tempstr


	def get_id_list(self, all_id=False, **params):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			if not all_id:
				cursor.execute("SELECT Id FROM main_table WHERE"+self.get_condition_sql_format(**params))
			else:
				cursor.execute("SELECT Id FROM main_table")
			templist=list(cursor)
			for i in range(0,len(templist)):
				templist[i]=templist[i][0]
			return templist


	def create_experiment(self,**params):
		return Experiment(database=self,**params)

	def commit(self,exp):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			binary=sql.Binary(bz2.compress(cPickle.dumps(exp,self.pickle_protocol)))
			cursor.execute("SELECT Modif_Time FROM main_table WHERE Id=\'"+exp.uuid+"\'")
			tempmodif=cursor.fetchone()
			if not tempmodif:
				cursor.execute("INSERT INTO main_table VALUES(?,?,?,?,?,?,?)", (\
					exp.uuid, \
					exp.init_time, \
					exp.modif_time, \
					str(exp._pop_cfg), \
#					exp._voctype, \
#					exp._strat["strattype"], \
#					exp._M, \
#					exp._W, \
#					exp._nbagent, \
					exp._T[-1], \
					exp._time_step, \
					binary,))
			elif tempmodif<exp.modif_time:
				cursor.execute("UPDATE main_table SET "\
					+"Modif_Time=\'"+str(exp.modif_time)+"\', "\
					+"Tmax=\'"+str(exp._T[-1])+"\', "\
					+"step=\'"+str(exp._time_step)+"\', "\
					+"Experiment_object=? WHERE Id=\'"+str(exp.uuid)+"\'",(binary,))\

	def commit_data(self,exp,graph,method):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			cursor.execute("SELECT Modif_Time FROM computed_data_table WHERE Id=\'"+exp.uuid+"\' AND Function=\'"+method+"\'")
			tempmodif=cursor.fetchall()
			if not tempmodif:
				binary=sql.Binary(bz2.compress(cPickle.dumps(graph,self.pickle_protocol)))
				cursor.execute("INSERT INTO computed_data_table VALUES(?,?,?,?,?)", (\
					exp.uuid, \
					graph.init_time, \
					graph.modif_time, \
					method, \
					binary,))
			elif tempmodif!=graph.modif_time:
				binary=sql.Binary(bz2.compress(cPickle.dumps(graph,self.pickle_protocol)))
				cursor.execute("UPDATE computed_data_table SET "\
					+"Modif_Time=\'"+graph.modif_time+"\', "\
					+"Custom_Graph=? WHERE Id=\'"+exp.uuid+"\' AND Function=\'"+method+"\'",(binary,))\

	def data_exists(self,nb_id,method):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			cursor.execute("SELECT Id FROM computed_data_table WHERE Id=\'"+nb_id+"\' AND Function=\'"+method+"\'")
			if cursor.fetchall():
				return True
			else:
				return False

class Experiment(ngsimu.Experiment):

	def __init__(self,pop_cfg,step=1,database=None):
		if not database:
			self.db=NamingGamesDB()
		else:
			self.db=database
		super(self.__class__,self).__init__(pop_cfg,step)

	def commit_to_db(self):
		self.db.commit(self)

	def commit_data_to_db(self,graph,method):
		self.db.commit_data(self,graph,method)

	def continue_exp_until(self,T,**kwargs):
		super(self.__class__,self).continue_exp_until(T,**kwargs)
		self.commit_to_db()

	def continue_exp(self,dT,**kwargs):
		self.continue_exp_until(self._T[-1]+dT,**kwargs)

	def graph(self,method="srtheo",X=None,tmin=0,tmax=None):
		if not tmax:
			tmax=self._T[-1]
		ind=-1
		while self._T[ind]>tmax:
			ind-=1
		if self.db.data_exists(nb_id=self.uuid,method=method):
			tempgraph=self.db.get_graph(self.uuid,method=method)
			if tempgraph._X[0][-1]<tmax:
				temptmin=self._T[len(tempgraph._X[0])]
				tempgraph2=super(self.__class__,self).graph(method=method,tmin=temptmin,tmax=tmax)
				tempgraph.complete_with(tempgraph2)
		else:
			tempgraph=super(self.__class__,self).graph(method=method,tmax=tmax)
		self.commit_data_to_db(tempgraph,method)
		if X:
			tempgraph2=self.graph(method=X,tmin=tmin,tmax=tmax)
			tempgraph=tempgraph.func_of(tempgraph2)
		return tempgraph


