#!/usr/bin/python

import os
import sqlite3 as sql
import sqlitebck
import time
import lzo
import cPickle
import json
from copy import deepcopy
import random
import uuid

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph

from . import ngmeth
from . import ngsimu

from weakref import WeakSet

class NamingGamesDB(object):

	def __new__(cls, inst_uuid=None, *args, **kwargs):
		if "instances" not in cls.__dict__:
			cls.instances = WeakSet()
		if inst_uuid is not None:
			for inst in cls.instances:
				if hasattr(inst,'uuid') and inst_uuid == inst.uuid:
					inst.just_retrieved = True
					return inst
		instance = object.__new__(cls, *args, **kwargs)
		cls.instances.add(instance)
		return instance

	def __getnewargs__(self):
		if hasattr(self,'uuid'):
			return (self.uuid,)
		else:
			return ()

	def __init__(self,path=None,do_not_close=False):
		if not hasattr(self,'uuid'):
			self.do_not_close = do_not_close
			self.uuid = str(uuid.uuid1())
			if not path:
				path='naminggames.db'
			self.dbpath = path
			self.name = os.path.basename(path)
			try:
				self.connection = sql.connect(self.dbpath)
			except Exception as e:
				#raise
				raise Exception(self.dbpath)
			self.cursor = self.connection.cursor()
			self.cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
					+"Id TEXT, "\
					+"Creation_Time INT, "\
					+"Modif_Time INT, "\
					+"Exec_Time INT, "\
					+"Config TEXT, "\
					+"Tmax INT, "\
					+"step INT, "\
					+"Experiment_object BLOB)")
			self.cursor.execute("CREATE TABLE IF NOT EXISTS computed_data_table("\
					+"Id TEXT, "\
					+"Creation_Time INT, "\
					+"Modif_Time INT, "\
					+"Expe_config TEXT, "\
					+"Function TEXT, "\
					+"Time_max INT, "\
					+"Custom_Graph BLOB)")
			self.connection.commit()

	def execute(self,command):
		self.cursor.execute(command)

	def reconnect(self,RAM_only=False):
		if RAM_only:
			self.connection = sql.connect('file:' + self.uuid + '?mode=memory&cache=shared',uri=True)#':memory:'
			self.cursor = self.connection.cursor()
		else:
			try:
				self.connection = sql.connect(self.dbpath)
			except sql.OperationalError:
				self.connection = sql.connect(self.name)
			self.cursor = self.connection.cursor()



	def move_to_RAM(self):
		if not hasattr(self,'old_conn'):
			self.connection.commit()
			self.old_conn = self.connection
			self.old_cur = self.cursor
			self.connection = sql.connect(':memory:')#'file:' + self.uuid + '?mode=memory&cache=shared',uri=True)
			self.cursor = self.connection.cursor()
			sqlitebck.copy(self.old_conn,self.connection)

	def commit_from_RAM(self):
		if hasattr(self,'old_conn'):
			self.connection.commit()
			sqlitebck.copy(self.connection, self.old_conn)

	def get_back_from_RAM(self):
		if hasattr(self,'old_conn'):
			self.commit_from_RAM()
			self.connection.close()
			self.connection = self.old_conn
			self.cursor = self.old_cur
			delattr(self,'old_cur')
			delattr(self,'old_conn')

	def close(self,force=False):
		if not self.do_not_close or force:
			if hasattr(self,'old_conn'):
				self.old_conn.close()
				delattr(self,'old_cur')
				delattr(self,'old_conn')
			if hasattr(self,'connection'):
				self.connection.close()
				delattr(self,'cursor')
				delattr(self,'connection')



	def merge(self, other_db, id_list=None, remove=False, main_only=False):
		if id_list is None:
			id_list=other_db.get_id_list(all_id=True)
		for xp_uuid in id_list:
			if self.id_in_db(xp_uuid) and (self.get_modif_time(xp_uuid)<other_db.get_modif_time(xp_uuid)):
				self.commit(other_db.get_experiment(xp_uuid=xp_uuid))
				#these few lines would be seen as repetitive and unnecessary, but for large databases it avoids loading all experiment objects, just the needed ones
			elif not self.id_in_db(xp_uuid):
				self.commit(other_db.get_experiment(xp_uuid=xp_uuid))
		if not main_only:
			for xp_uuid in id_list:
				other_methd_list=other_db.get_method_list(xp_uuid)
				methd_list=self.get_method_list(xp_uuid)
				for met in other_methd_list:
					if (met in methd_list) and (self.get_modif_time(xp_uuid,graph=met)<other_db.get_modif_time(xp_uuid,graph=met)):
						self.commit_data(other_db.get_experiment(xp_uuid=xp_uuid),other_db.get_graph(xp_uuid,method=met),met)
					elif not (met in methd_list):
						self.commit_data(other_db.get_experiment(xp_uuid=xp_uuid),other_db.get_graph(xp_uuid,method=met),met)
		if remove:
			os.remove(other_db.dbpath)
		self.connection.commit()

	def export(self, other_db, id_list=None, methods=[],graph_only=False):
		if id_list is None:
			id_list = self.get_id_list()
		#with sql.connect(other_db.dbpath, isolation_level=None):
		other_cursor = other_db.cursor #sql.connect(other_db.dbpath, isolation_level=None).cursor()
		for xp_uuid in id_list:
			if not graph_only:
				self.cursor.execute("SELECT * FROM main_table WHERE Id=\'"+str(xp_uuid)+"\'")
				xp_data = self.cursor.fetchone()
				if not xp_uuid in other_db.get_id_list():
					other_cursor.execute("INSERT INTO main_table VALUES (?,?,?,?,?,?,?,?)",(xp_data))
				elif self.get_param(xp_uuid=xp_uuid, param='Tmax') > other_db.get_param(xp_uuid=xp_uuid, param='Tmax'):
					other_cursor.execute("DELETE FROM main_table WHERE Id=\'"+str(xp_uuid)+"\'")
					other_cursor.execute("INSERT INTO main_table VALUES (?,?,?,?,?,?,?,?)",(xp_data))
			for method in methods:
				if self.data_exists(xp_uuid=xp_uuid, method=method):
					self.cursor.execute("SELECT * FROM computed_data_table WHERE Id=\'"+str(xp_uuid)+"\' AND Function= \'"+method+"\'")
					gr_data = self.cursor.fetchone()
					if not other_db.data_exists(xp_uuid=xp_uuid, method=method):
						other_cursor.execute("INSERT INTO computed_data_table VALUES (?,?,?,?,?,?,?)",(gr_data))
					elif self.get_param(xp_uuid=xp_uuid, method=method, param='Time_max') > other_db.get_param(xp_uuid=xp_uuid, method=method, param='Time_max'):
						other_cursor.execute("DELETE FROM computed_data_table WHERE Id=\'"+str(xp_uuid)+"\' AND Function= \'"+method+"\'")
						other_cursor.execute("INSERT INTO computed_data_table VALUES (?,?,?,?,?,?,?)",(gr_data))
		other_db.connection.commit()

	def delete(self, id_list, graph_only=False, xp_only=False, met=''):
		if met:
			met = ' AND Function=\'{}\''.format(met)
		if graph_only:
			for xp_uuid in id_list:
				self.cursor.execute("DELETE FROM computed_data_table WHERE Id=\'{}\'".format(str(xp_uuid)+met))
		else:
			for xp_uuid in id_list:
				if not xp_only:
					self.cursor.execute("DELETE FROM computed_data_table WHERE Id=\'{}\'".format(str(xp_uuid)+met))
				self.cursor.execute("DELETE FROM main_table WHERE Id=\'{}\'".format(str(xp_uuid)))
				try:
					os.remove(os.path.join(os.path.dirname(self.dbpath),'data',xp_uuid+'.db'))
				except OSError:
					pass
				try:
					os.remove(os.path.join(os.path.dirname(self.dbpath),'data',xp_uuid+'.db.xz'))
				except OSError:
					pass
		self.connection.commit()



	def get_method_list(self,xp_uuid):
		self.cursor.execute("SELECT Function FROM computed_data_table WHERE Id=\'"+str(xp_uuid)+"\'")
		templist=list(self.cursor)
		for i in range(0,len(templist)):
			templist[i]=templist[i][0]
		return templist

	def get_modif_time(self,xp_uuid,graph=None):
		if not graph:
			self.cursor.execute("SELECT Modif_Time FROM main_table WHERE Id=\'"+str(xp_uuid)+"\'")
			return self.cursor.fetchone()[0]
		else:
			self.cursor.execute("SELECT Modif_Time FROM computed_data_table WHERE Id=\'"+str(xp_uuid)+"\' AND Function=\'"+graph+"\'")
			return self.cursor.fetchone()[0]

	def id_in_db(self,xp_uuid):
		self.cursor.execute("SELECT Id FROM main_table WHERE Id=\'"+str(xp_uuid)+"\'")
		if self.cursor.fetchall():
			return True
		else:
			return False

	def get_experiment(self, xp_uuid=None, force_new=False, blacklist=[], pattern=None, tmax=0, **xp_cfg):
		if force_new:
			tempexp = Experiment(database=self,**xp_cfg)
			tempexp.commit_to_db()
		elif xp_uuid is not None:
			if self.id_in_db(xp_uuid):
				self.cursor.execute("SELECT Experiment_object FROM main_table WHERE Id=\'"+str(xp_uuid)+"\'")
				tempblob = self.cursor.fetchone()
				tempexp = cPickle.loads(lzo.decompress(str(tempblob[0])))
				tempexp.db = self
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
			for xp_uuid in templist:
				t = int(self.get_param(param='Tmax', xp_uuid=xp_uuid))
				temptmax = max(temptmax, min(t ,tmax))
			for xp_uuid in templist:
				t = int(self.get_param(param='Tmax', xp_uuid=xp_uuid))
				if t < temptmax:
					templist.remove(xp_uuid)
			if templist:
				i=random.randint(0,len(templist)-1)
				tempexp = self.get_experiment(xp_uuid=templist[i])
				tempexp.db=self
			else:
				tempexp = Experiment(database=self,**xp_cfg)
				tempexp.commit_to_db()
		return tempexp


	def get_graph(self,xp_uuid=None,xp_cfg=None,method="srtheo",tmin=0,tmax=None):
		self.cursor.execute("SELECT Custom_Graph FROM computed_data_table WHERE Id=\'"+str(xp_uuid)+"\' AND Function=\'"+method+"\'")
		tempblob = self.cursor.fetchone()
		return cPickle.loads(lzo.decompress(str(tempblob[0])))
		#TODO: implement dealing with xp_cfg


	def get_graph_id_list(self,xp_cfg,method="srtheo",tmax=None):
		if tmax is None:
			self.cursor.execute("SELECT Id FROM computed_data_table WHERE Expe_config=\'"+json.dumps(xp_cfg, sort_keys=True)+"\' AND Function=\'"+method+"\'")
			templist=list(self.cursor)
			for i in range(0,len(templist)):
				templist[i]=templist[i][0]
			return templist
		else:
			self.cursor.execute("SELECT Id FROM computed_data_table WHERE Expe_config=\'"+json.dumps(xp_cfg, sort_keys=True)+"\' AND Function=\'"+method+"\' AND Time_max>=\'"+tmax+"\'")
			templist=list(self.cursor)
			for i in range(0,len(templist)):
				templist[i]=templist[i][0]
			if templist:
				return templist
			elif tmax < 0:
				return []
			else:
				self.cursor.execute("SELECT Time_max FROM computed_data_table WHERE Expe_config=\'"+json.dumps(xp_cfg, sort_keys=True)+"\' AND Function=\'"+method+"\'")
				templist=list(self.cursor)
				for i in range(0,len(templist)):
					templist[i]=templist[i][0]
				return self.get_graph_id_list(xp_cfg=xp_cfg,method=method,tmax=t_max)
		#TODO: implement generator instead of list??





	def get_id_list(self, all_id=False, pattern=None, tmax=0, **xp_cfg):
		if (not all_id) and (xp_cfg or pattern):
			if xp_cfg:
				self.cursor.execute("SELECT Id FROM main_table WHERE Config=\'{}\'".format(json.dumps(xp_cfg, sort_keys=True)))
			else:
				self.cursor.execute("SELECT Id FROM main_table WHERE Config LIKE \'{}\'".format(pattern))
		else:
			self.cursor.execute("SELECT Id FROM main_table")
		templist=list(self.cursor)
		for i in range(0,len(templist)):
			templist[i]=templist[i][0]
		return templist
		#TODO: implement generator instead of list??

	def get_param(self, xp_uuid, param, method=None):
		if method is None:
			self.cursor.execute("SELECT {} FROM {} WHERE Id=\'{}\'".format(param, 'main_table', xp_uuid))
		else:
			self.cursor.execute("SELECT {} FROM {} WHERE Id=\'{}\' and Function=\'{}\'".format(param, 'computed_data_table', xp_uuid, method))
		temp = self.cursor.fetchone()
		return temp[0]

	def create_experiment(self,**xp_cfg):
		return Experiment(database=self,**xp_cfg)

	def commit(self,exp):
		binary=sql.Binary(lzo.compress(cPickle.dumps(exp,cPickle.HIGHEST_PROTOCOL)))
		if not exp._exec_time:
			exec_time = -1
		else:
			exec_time = exp._exec_time[-1]
		if not exp._T:
			T = -1
		else:
			T = exp._T[-1]
		try:
			self.cursor.execute("SELECT Tmax FROM main_table WHERE Id=\'"+exp.uuid+"\'")
		except:
			print exp.uuid
			print self.dbpath
			print os.getcwd()
			raise
		tempmodiftup = self.cursor.fetchone()
		if not tempmodiftup:

			self.cursor.execute("INSERT INTO main_table VALUES(?,?,?,?,?,?,?,?)", (\
				exp.uuid, \
				exp.init_time, \
				exp.modif_time, \
				exec_time, \
				json.dumps({'pop_cfg':exp._pop_cfg, 'step':exp._time_step}, sort_keys=True), \
		#		exp._voctype, \
		#		exp._strat["strattype"], \
		#		exp._M, \
		#		exp._W, \
		#		exp._nbagent, \
				T, \
				exp._time_step, \
				binary,))
		#elif tempmodiftup[0]<exp.modif_time:
		elif tempmodiftup[0]<T:
			self.cursor.execute("UPDATE main_table SET "\
				+"Modif_Time=\'"+str(exp.modif_time)+"\', "\
				+"Exec_Time=\'"+str(exec_time)+"\', "\
				+"Tmax=\'"+str(T)+"\', "\
				+"step=\'"+str(exp._time_step)+"\', "\
				+"Experiment_object=? WHERE Id=\'"+str(exp.uuid)+"\'",(binary,))
		self.connection.commit()

	def commit_data(self,exp,graph,method):
		self.cursor.execute("SELECT Modif_Time FROM computed_data_table WHERE Id=\'"+exp.uuid+"\' AND Function=\'"+method+"\'")
		tempmodiftup = self.cursor.fetchone()
		self.cursor.execute("SELECT Time_max FROM computed_data_table WHERE Id=\'"+exp.uuid+"\' AND Function=\'"+method+"\'")
		tempmodiftup2 = self.cursor.fetchone()
		if not tempmodiftup:
			if not graph._X[0][0] == 0 and self.data_exists(xp_uuid=exp.uuid,method=method):
				graph.complete_with(self.get_graph(exp.uuid,graph,method))
			binary=sql.Binary(lzo.compress(cPickle.dumps(graph,cPickle.HIGHEST_PROTOCOL)))
			self.cursor.execute("INSERT INTO computed_data_table VALUES(?,?,?,?,?,?,?)", (\
				exp.uuid, \
				graph.init_time, \
				graph.modif_time, \
				json.dumps({'pop_cfg':exp._pop_cfg, 'step':exp._time_step}, sort_keys=True), \
				method, \
				graph._X[0][-1], \
				binary,))
		elif tempmodiftup[0]!=graph.modif_time and graph._X[0][-1]>tempmodiftup2[0]:
			binary=sql.Binary(lzo.compress(cPickle.dumps(graph,cPickle.HIGHEST_PROTOCOL)))
			self.cursor.execute("UPDATE computed_data_table SET "\
				+"Modif_Time=\'"+str(graph.modif_time)+"\', "\
				+"Time_max=\'"+str(graph._X[0][-1])+"\', "\
				+"Custom_Graph=? WHERE Id=\'"+str(exp.uuid)+"\' AND Function=\'"+method+"\'",(binary,))
		self.connection.commit()

	def data_exists(self,xp_uuid,method):
		self.cursor.execute("SELECT Id FROM computed_data_table WHERE Id=\'"+xp_uuid+"\' AND Function=\'"+method+"\'")
		if self.cursor.fetchall():
			return True
		else:
			return False

	def graph(self, cfg=[], nb_iter=1, uuid_list=[]):
		pass

	def __getstate__(self):
		out_dict = self.__dict__.copy()
		if hasattr(self,'connection'):
			self.connection.commit()
			del out_dict['cursor']
			del out_dict['connection']
		if hasattr(self,'old_conn'):
			del out_dict['old_conn']
			del out_dict['old_cur']
		return out_dict

	def __setstate__(self, in_dict):
		if not hasattr(self,'just_retrieved'):
			in_dict['do_not_close'] = False
			self.__dict__.update(in_dict)
		else:
			delattr(self,'just_retrieved')
		#self.connection = sql.connect(self.dbpath)
		#self.cursor = self.connection.cursor()


class Experiment(ngsimu.Experiment):

	def __init__(self,pop_cfg,step=1,database=None,compute=True):
		if not database:
			self.db = NamingGamesDB()
		else:
			self.db = database
		self.compute = compute
		super(Experiment,self).__init__(pop_cfg,step)
		self.commit_to_db(rm=True)

	def commit_to_db(self,rm=False):
		self.db.commit(self)
		filepath = self._poplist.filepath
		if os.path.isfile(filepath):
			self.compress(rm=rm)

	def commit_data_to_db(self,graph,method):
		self.db.commit_data(self,graph,method)

	def continue_exp_until(self,T, autocommit=True):
		if not self.compute and T >= self._T[-1] + self.stepfun(self._T[-1]):
			raise Exception('Computation needed')
		try:
			super(Experiment,self).continue_exp_until(T)
		except:
			print self.uuid
			raise
		if autocommit:
			self.commit_to_db()

	def continue_exp(self,dT=None, autocommit=True):
		if not self._T:
			self.add_pop(ngsimu.Population(**self._pop_cfg),0)
		if dT is None:
			dT = self.stepfun(self._T[-1])
		self.continue_exp_until(self._T[-1]+dT, autocommit=autocommit)

	def graph(self,method="srtheo", X=None, tmin=0, tmax=None, autocommit=True, tempgraph=None):
		do_not_commit = False
		if not tmax:
			tmax = self._T[-1]
		ind = -1
		if tmax >= self._T[-1] + self.stepfun(self._T[-1]):
			if not self.compute:
				raise Exception('Computation needed')
			self.continue_exp_until(tmax, autocommit=autocommit)
			return self.graph(method=method, X=X, tmin=tmin, tmax=tmax, autocommit=autocommit, tempgraph=tempgraph)
		while self._T[ind]>tmax:
			ind -= 1
		if self.db.data_exists(xp_uuid=self.uuid, method=method):
			if tempgraph is None:
				tempgraph = self.db.get_graph(self.uuid, method=method)
			#dbmin = tempgraph._X[0][0] - self._time_step
			dbmax = tempgraph._X[0][-1] + self.stepfun(tempgraph._X[0][-1])
			if dbmax>=tmin: #and dbmin<=tmax
				if dbmax<tmax:
					if not self.compute:
						raise Exception('Computation needed')
					temptmin = max(dbmax,tmin)
					tempgraph2 = super(Experiment,self).graph(method=method, tmin=temptmin, tmax=tmax)
					cust_func = getattr(ngmeth,'custom_'+method)# avoiding having several values for exp level
					if cust_func.level != 'exp':
						tempgraph.complete_with(tempgraph2)
				if not len(tempgraph._X)==1: # for data at exp level
					while tmax < tempgraph._X[0][-1]:
						do_not_commit = True
						tempgraph._X[0].pop()
						tempgraph._Y[0].pop()
						tempgraph.stdvec[0].pop()
					while tmin > tempgraph._X[0][0]:
						do_not_commit = True
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
			if do_not_commit:
				raise Exception('trying to commit a reduced version of graph')
			self.commit_data_to_db(tempgraph,method)
		if X:
			tempgraph2 = self.graph(method=X, tmin=tmin, tmax=tmax, autocommit=autocommit)
			tempgraph = tempgraph.func_of(tempgraph2)
		return tempgraph
