#!/usr/bin/python

import os
import sqlite3 as sql
import time
import bz2
import cPickle
import json
from copy import deepcopy
import random

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph

from . import ngmeth
from . import ngsimu

class NamingGamesDB(object):
	def __init__(self,path=None):
		if not path:
			path='naminggames.db'
		self.dbpath=path
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
				+"Id TEXT, "\
				+"Creation_Time INT, "\
				+"Modif_Time INT, "\
				+"Exec_Time INT, "\
				+"Config TEXT, "\
				+"Tmax INT, "\
				+"step INT, "\
				+"Experiment_object BLOB)")
			cursor.execute("CREATE TABLE IF NOT EXISTS computed_data_table("\
				+"Id TEXT, "\
				+"Creation_Time INT, "\
				+"Modif_Time INT, "\
				+"Expe_config TEXT, "\
				+"Function TEXT, "\
				+"Time_max INT, "\
				+"Custom_Graph BLOB)")

	def merge(self, other_db, id_list=None, remove=False, main_only=False):
		if id_list is None:
			id_list=other_db.get_id_list(all_id=True)
		for uuid in id_list:
			if self.id_in_db(uuid) and (self.get_modif_time(uuid)<other_db.get_modif_time(uuid)):
				self.commit(other_db.get_experiment(uuid=uuid))
				#these few lines would be seen as repetitive and unnecessary, but for large databases it avoids loading all experiment objects, just the needed ones
			elif not self.id_in_db(uuid):
				self.commit(other_db.get_experiment(uuid=uuid))
		if not main_only:
			for uuid in id_list:
				other_methd_list=other_db.get_method_list(uuid)
				methd_list=self.get_method_list(uuid)
				for met in other_methd_list:
					if (met in methd_list) and (self.get_modif_time(uuid,graph=met)<other_db.get_modif_time(uuid,graph=met)):
						self.commit_data(other_db.get_experiment(uuid=uuid),other_db.get_graph(uuid,method=met),met)
					elif not (met in methd_list):
						self.commit_data(other_db.get_experiment(uuid=uuid),other_db.get_graph(uuid,method=met),met)
		if remove:
			os.remove(other_db.dbpath)

	def export(self, other_db, id_list=None, methods=[],graph_only=False):
		if id_list is None:
			id_list = self.get_id_list()
		with sql.connect(self.dbpath):
			cursor = sql.connect(self.dbpath).cursor()
			with sql.connect(other_db.dbpath, isolation_level=None):
				other_cursor = sql.connect(other_db.dbpath, isolation_level=None).cursor()
				for uuid in id_list:
					if not graph_only:
						cursor.execute("SELECT * FROM main_table WHERE Id=\'"+str(uuid)+"\'")
						xp_data = cursor.fetchone()
						if not uuid in other_db.get_id_list():
							other_cursor.execute("INSERT INTO main_table VALUES (?,?,?,?,?,?,?,?)",(xp_data))
						elif self.get_param(uuid=uuid, param='Tmax') > other_db.get_param(uuid=uuid, param='Tmax'):
							other_cursor.execute("DELETE FROM main_table WHERE Id=\'"+str(uuid)+"\'")
							other_cursor.execute("INSERT INTO main_table VALUES (?,?,?,?,?,?,?,?)",(xp_data))
					for method in methods:
						if self.data_exists(uuid=uuid, method=method):
							cursor.execute("SELECT * FROM computed_data_table WHERE Id=\'"+str(uuid)+"\' AND Function= \'"+method+"\'")
							gr_data = cursor.fetchone()
							if not other_db.data_exists(uuid=uuid, method=method):
								other_cursor.execute("INSERT INTO computed_data_table VALUES (?,?,?,?,?,?,?)",(gr_data))
							elif self.get_param(uuid=uuid, method=method, param='Time_max') > other_db.get_param(uuid=uuid, method=method, param='Time_max'):
								other_cursor.execute("DELETE FROM computed_data_table WHERE Id=\'"+str(uuid)+"\' AND Function= \'"+method+"\'")
								other_cursor.execute("INSERT INTO computed_data_table VALUES (?,?,?,?,?,?,?)",(gr_data))

	def delete(self, id_list, graph_only=False, met=''):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			if met:
				met = ' AND Function=\'{}\''.format(met)
			if graph_only:
				for uuid in id_list:
					cursor.execute("DELETE FROM computed_data_table WHERE Id=\'{}\'".format(str(uuid)+met))
			else:
				for uuid in id_list:
					cursor.execute("DELETE FROM computed_data_table WHERE Id=\'{}\'".format(str(uuid)+met))
					cursor.execute("DELETE FROM main_table WHERE Id=\'{}\'".format(str(uuid)))


	def get_method_list(self,uuid):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			cursor.execute("SELECT Function FROM computed_data_table WHERE Id=\'"+str(uuid)+"\'")
			templist=list(cursor)
			for i in range(0,len(templist)):
				templist[i]=templist[i][0]
			return templist

	def get_modif_time(self,uuid,graph=None):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			if not graph:
				cursor.execute("SELECT Modif_Time FROM main_table WHERE Id=\'"+str(uuid)+"\'")
				return cursor.fetchone()[0]
			else:
				cursor.execute("SELECT Modif_Time FROM computed_data_table WHERE Id=\'"+str(uuid)+"\' AND Function=\'"+graph+"\'")
				return cursor.fetchone()[0]

	def id_in_db(self,uuid):
		with sql.connect(self.dbpath):
			cursor=sql.connect(self.dbpath).cursor()
			cursor.execute("SELECT Id FROM main_table WHERE Id=\'"+str(uuid)+"\'")
			if cursor.fetchall():
				return True
			else:
				return False

	def get_experiment(self, uuid=None, force_new=False, blacklist=[], pattern=None, tmax=0, **xp_cfg):
		if force_new:
			tempexp = Experiment(database=self,**xp_cfg)
			tempexp.commit_to_db()
		elif uuid is not None:
			if self.id_in_db(uuid):
				conn=sql.connect(self.dbpath)
				with conn:
					cursor=conn.cursor()
					cursor.execute("SELECT Experiment_object FROM main_table WHERE Id=\'"+str(uuid)+"\'")
					tempblob=cursor.fetchone()
					tempexp = cPickle.loads(bz2.decompress(str(tempblob[0])))
					tempexp.db=self
			else:
				print("ID doesn't exist in DB")
				return self.get_experiment(blacklist=blacklist,pattern=pattern,tmax=tmax, **xp_cfg)
		else:
			templist=self.get_id_list(pattern=pattern, tmax=tmax, **xp_cfg)
			for elt in blacklist:
				try:
					templist.remove(elt)
				except ValueError:
					pass
			temptmax = -1
			for uuid in templist:
				t = int(self.get_param(param='Tmax', uuid=uuid))
				temptmax = max(temptmax, min(t ,tmax))
			for uuid in templist:
				t = int(self.get_param(param='Tmax', uuid=uuid))
				if t < temptmax:
					templist.remove(uuid)
			if templist:
				i=random.randint(0,len(templist)-1)
				tempexp = self.get_experiment(uuid=templist[i])
				tempexp.db=self
			else:
				tempexp = Experiment(database=self,**xp_cfg)
				tempexp.commit_to_db()
		return tempexp


	def get_graph(self,uuid=None,xp_cfg=None,method="srtheo",tmin=0,tmax=None):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			cursor.execute("SELECT Custom_Graph FROM computed_data_table WHERE Id=\'"+str(uuid)+"\' AND Function=\'"+method+"\'")
			tempblob=cursor.fetchone()
			return cPickle.loads(bz2.decompress(str(tempblob[0])))
		#TODO: implement dealing with xp_cfg


	def get_graph_id_list(self,xp_cfg,method="srtheo",tmax=None):
		conn=sql.connect(self.dbpath)
		with conn:
				cursor=conn.cursor()
				if tmax is None:
					cursor.execute("SELECT Id FROM computed_data_table WHERE Expe_config=\'"+json.dumps(xp_cfg, sort_keys=True)+"\' AND Function=\'"+method+"\'")
					templist=list(cursor)
					for i in range(0,len(templist)):
						templist[i]=templist[i][0]
					return templist
				else:
					cursor.execute("SELECT Id FROM computed_data_table WHERE Expe_config=\'"+json.dumps(xp_cfg, sort_keys=True)+"\' AND Function=\'"+method+"\' AND Time_max>=\'"+tmax+"\'")
					templist=list(cursor)
					for i in range(0,len(templist)):
						templist[i]=templist[i][0]
					if templist:
						return templist
					elif tmax < 0:
						return []
					else:
						cursor.execute("SELECT Time_max FROM computed_data_table WHERE Expe_config=\'"+json.dumps(xp_cfg, sort_keys=True)+"\' AND Function=\'"+method+"\'")
						templist=list(cursor)
						for i in range(0,len(templist)):
							templist[i]=templist[i][0]
						return self.get_graph_id_list(xp_cfg=xp_cfg,method=method,tmax=t_max)
		#TODO: implement generator instead of list??





	def get_id_list(self, all_id=False, pattern=None, tmax=0, **xp_cfg):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			if (not all_id) and (xp_cfg or pattern):
				if xp_cfg:
					cursor.execute("SELECT Id FROM main_table WHERE Config=\'{}\'".format(json.dumps(xp_cfg, sort_keys=True)))
				else:
					cursor.execute("SELECT Id FROM main_table WHERE Config LIKE \'{}\'".format(pattern))
			else:
				cursor.execute("SELECT Id FROM main_table")
			templist=list(cursor)
			for i in range(0,len(templist)):
				templist[i]=templist[i][0]
			return templist
		#TODO: implement generator instead of list??

	def get_param(self, uuid, param, method=None):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			if method is None:
				cursor.execute("SELECT {} FROM {} WHERE Id=\'{}\'".format(param, 'main_table', uuid))
			else:
				cursor.execute("SELECT {} FROM {} WHERE Id=\'{}\' and Function=\'{}\'".format(param, 'computed_data_table', uuid, method))
			temp = cursor.fetchone()
			return temp[0]

	def create_experiment(self,**xp_cfg):
		return Experiment(database=self,**xp_cfg)

	def commit(self,exp):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			binary=sql.Binary(bz2.compress(cPickle.dumps(exp,cPickle.HIGHEST_PROTOCOL)))
			try:
				cursor.execute("SELECT Tmax FROM main_table WHERE Id=\'"+exp.uuid+"\'")
			except:
				print exp.uuid
				print self.dbpath
				print os.getcwd()
				raise
			tempmodiftup=cursor.fetchone()
			if not tempmodiftup:
				cursor.execute("INSERT INTO main_table VALUES(?,?,?,?,?,?,?,?)", (\
					exp.uuid, \
					exp.init_time, \
					exp.modif_time, \
					exp._exec_time[-1], \
					json.dumps({'pop_cfg':exp._pop_cfg, 'step':exp._time_step}, sort_keys=True), \
#					exp._voctype, \
#					exp._strat["strattype"], \
#					exp._M, \
#					exp._W, \
#					exp._nbagent, \
					exp._T[-1], \
					exp._time_step, \
					binary,))
			#elif tempmodiftup[0]<exp.modif_time:
			elif tempmodiftup[0]<exp._T[-1]:
				cursor.execute("UPDATE main_table SET "\
					+"Modif_Time=\'"+str(exp.modif_time)+"\', "\
					+"Exec_Time=\'"+str(exp._exec_time[-1])+"\', "\
					+"Tmax=\'"+str(exp._T[-1])+"\', "\
					+"step=\'"+str(exp._time_step)+"\', "\
					+"Experiment_object=? WHERE Id=\'"+str(exp.uuid)+"\'",(binary,))\

	def commit_data(self,exp,graph,method):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			cursor.execute("SELECT Modif_Time FROM computed_data_table WHERE Id=\'"+exp.uuid+"\' AND Function=\'"+method+"\'")
			tempmodiftup=cursor.fetchone()
			cursor.execute("SELECT Time_max FROM computed_data_table WHERE Id=\'"+exp.uuid+"\' AND Function=\'"+method+"\'")
			tempmodiftup2=cursor.fetchone()
			if not tempmodiftup:
				if not graph._X[0][0] == 0:
					graph.complete_with(self.get_graph(exp,graph,method))
				binary=sql.Binary(bz2.compress(cPickle.dumps(graph,cPickle.HIGHEST_PROTOCOL)))
				cursor.execute("INSERT INTO computed_data_table VALUES(?,?,?,?,?,?,?)", (\
					exp.uuid, \
					graph.init_time, \
					graph.modif_time, \
					json.dumps({'pop_cfg':exp._pop_cfg, 'step':exp._time_step}, sort_keys=True), \
					method, \
					graph._X[0][-1], \
					binary,))
			elif tempmodiftup[0]!=graph.modif_time and graph._X[0][-1]>tempmodiftup2[0]:
				binary=sql.Binary(bz2.compress(cPickle.dumps(graph,cPickle.HIGHEST_PROTOCOL)))
				cursor.execute("UPDATE computed_data_table SET "\
					+"Modif_Time=\'"+str(graph.modif_time)+"\', "\
					+"Time_max=\'"+str(graph._X[0][-1])+"\', "\
					+"Custom_Graph=? WHERE Id=\'"+str(exp.uuid)+"\' AND Function=\'"+method+"\'",(binary,))\

	def data_exists(self,uuid,method):
		conn=sql.connect(self.dbpath)
		with conn:
			cursor=conn.cursor()
			cursor.execute("SELECT Id FROM computed_data_table WHERE Id=\'"+uuid+"\' AND Function=\'"+method+"\'")
			if cursor.fetchall():
				return True
			else:
				return False

	def graph(self, cfg=[], nb_iter=1, uuid_list=[]):
		pass


class Experiment(ngsimu.Experiment):

	def __init__(self,pop_cfg,step=1,database=None,compute=True):
		if not database:
			self.db=NamingGamesDB()
		else:
			self.db=database
			self.compute = compute
		super(Experiment,self).__init__(pop_cfg,step)
		self.commit_to_db()

	def commit_to_db(self):
		self.db.commit(self)

	def commit_data_to_db(self,graph,method):
		self.db.commit_data(self,graph,method)

	def continue_exp_until(self,T, autocommit=True):
		if not self.compute and T >= self._T[-1] + self._time_step:
			raise Exception('Computation needed')
		super(Experiment,self).continue_exp_until(T)
		if autocommit:
			self.commit_to_db()

	def continue_exp(self,dT=None, autocommit=True):
		if dT is None:
			dT = self._time_step
		self.continue_exp_until(self._T[-1]+dT, autocommit=autocommit)

	def graph(self,method="srtheo", X=None, tmin=0, tmax=None, autocommit=True, tempgraph=None):
		if not tmax:
			tmax = self._T[-1]
		ind=-1
		if tmax >= self._T[-1] + self._time_step:
			if not self.compute:
				raise Exception('Computation needed')
			self.continue_exp_until(tmax, autocommit=autocommit)
			return self.graph(method=method, X=X, tmin=tmin, tmax=tmax, autocommit=autocommit, tempgraph=tempgraph)
		while self._T[ind]>tmax:
			ind-=1
		if self.db.data_exists(uuid=self.uuid, method=method):
			if tempgraph is None:
				tempgraph = self.db.get_graph(self.uuid, method=method)
			#dbmin = tempgraph._X[0][0] - self._time_step
			dbmax = tempgraph._X[0][-1] + self._time_step
			if dbmax>=tmin: #and dbmin<=tmax
				if dbmax<tmax:
					if not self.compute:
						raise Exception('Computation needed')
					temptmin = max(dbmax,tmin)
					tempgraph2 = super(Experiment,self).graph(method=method, tmin=temptmin, tmax=tmax)
					tempgraph.complete_with(tempgraph2)
				while tmax < tempgraph._X[0][-1]:
					tempgraph._X[0].pop()
					tempgraph._Y[0].pop()
					tempgraph.stdvec[0].pop()
				while tmin > tempgraph._X[0][0]:
					tempgraph._X[0].pop(0)
					tempgraph._Y[0].pop(0)
					tempgraph.stdvec[0].pop(0)
			else:
				if not self.compute:
					raise Exception('Computation needed')
				tempgraph = super(Experiment,self).graph(method=method, tmin=tmin, tmax=tmax)
		else:
			if not self.compute:
				raise Exception('Computation needed')
			tempgraph = super(Experiment, self).graph(method=method,tmin=tmin, tmax=tmax)
		if autocommit:
			self.commit_data_to_db(tempgraph,method)
		if X:
			tempgraph2 = self.graph(method=X, tmin=tmin, tmax=tmax, autocommit=autocommit)
			tempgraph = tempgraph.func_of(tempgraph2)
		return tempgraph
