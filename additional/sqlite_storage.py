import lzo
import os
import errno
try:
	import cPickle as pickle
except ImportError:
	import pickle
import sqlite3 as sql
import psycopg2
try:
	import lzma
except ImportError:
	import backports.lzma as lzma
import bz2
from shutil import copyfileobj

def xz_decompress(self,file):
	outfile = file[:-3]
	with open(outfile,'wb') as output:
		with lzma.LZMAFile(file,'rb') as uncompressed:
		#with bz2.BZ2File(file) as uncompressed:
		copyfileobj(uncompressed,output)

def xz_compress(self,file,rm=False):
	outfile = file+'.xz'
	#with open(outfile) as output:
	with open(file,'rb') as uncompressed:
		with lzma.LZMAFile(outfile,'wb') as compressed:
		#with bz2.BZ2File(outfile,'w') as compressed:
			copyfileobj(uncompressed,compressed)
	if rm:
		os.remove(file)

class SQLiteStorage(object):

	def __init__(self,filepath,db_id=None):
		self.filepath = filepath

	def add_data(self,data,label):
		if not os.path.isfile(self.filepath):
			if not os.path.isfile(self.filepath+'.xz'):
				raise IOError('No file for poplist: '+self.filepath+' . You should call init_db before adding elements')
			else:
				xz_decompress(self.filepath+'.xz')
		pickled_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
		lz_data = lzo.compress(pickled_data)
		conn = sql.connect(self.filepath)
		with conn:
			cursor = conn.cursor()
	#		cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
	#				+"T INT, "\
	#				+"Population_object BLOB)")
			cursor.execute("DELETE FROM main_table WHERE T="+str(label))
			cursor.execute("INSERT INTO main_table VALUES (?,?)",(label,sql.Binary(lz_data)))


	def read_data(self,label=None):
		if not os.path.isfile(self.filepath):
			if not os.path.isfile(self.filepath+'.xz'):
				raise IOError('No file for poplist: '+self.filepath+' . You should call init_db before adding elements')
			else:
				xz_decompress(self.filepath+'.xz')
		conn = sql.connect(self.filepath)
		with conn:
			cursor = conn.cursor()
			if label is None:
				cursor.execute('SELECT max(T) FROM main_table')
				max_T = cursor.fetchone()[0]
				label = max_T
			cursor.execute("SELECT Population_object FROM main_table WHERE T=\'"+str(label)+"\'")
			blob = cursor.fetchone()
		if blob is None:
			raise IOError('No row in database ' + str(self.filepath) + ' for label: '+str(label))
		lz_data = blob[0]
		pickled_data = lzo.decompress(lz_data)
		data = pickle.loads(pickled_data)
		return data

	def init_db(self):
		try:
			os.makedirs(os.path.dirname(self.filepath))
		except OSError as exc:
			if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(self.filepath)):
				pass
			else:
				raise
		conn = sql.connect(self.filepath)
		with conn:
			cursor = conn.cursor()
			cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
					+"T INT, "\
					+"Population_object BLOB)")



class PostgresStorage(SQLiteStorage):

	def __init__(self,db_id=None,conn_info=None):
		if db_id is None:
			self.db_id = str(uuid.uuid1())
		else:
			self.db_id = db_id
		if conn_info is None:
			self.conn_info = "host='localhost' dbname='naminggames' user='naminggames' password='naminggames'"
		else:
			self.conn_info = conn_info

	def init_db(self):
		conn = psycopg2.connect(self.conn_info)
		with conn:
			cursor = conn.cursor()
			cursor.execute("CREATE TABLE IF NOT EXISTS "+self.db_id+"("\
					+"T BIGINT, "\
					+"Population_object BYTEA)")



	def add_data(self,data,label):
		pickled_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
		lz_data = lzo.compress(pickled_data)
		conn = psycopg2.connect(self.conn_info)
		with conn:
			cursor = conn.cursor()
	#		cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
	#				+"T INT, "\
	#				+"Population_object BLOB)")
			cursor.execute("DELETE FROM "+self.db_id+" WHERE T="+str(label))
			cursor.execute("INSERT INTO "+self.db_id+" VALUES (%s,%s)",(label,psycopg2.Binary(lz_data)))


	def read_data(self,label=None):
		conn = psycopg2.connect(self.conn_info)
		with conn:
			cursor = conn.cursor()
			if label is None:
				cursor.execute('SELECT max(T) FROM '+self.db_id)
				max_T = cursor.fetchone()[0]
				label = max_T
			cursor.execute("SELECT Population_object FROM "+self.db_id+" WHERE T=\'"+str(label)+"\'")
			blob = cursor.fetchone()
		if blob is None:
			raise IOError('No row in database ' + self.db_id + ' for label: '+str(label))
		lz_data = blob[0]
		pickled_data = lzo.decompress(lz_data)
		data = pickle.loads(pickled_data)
		return data
