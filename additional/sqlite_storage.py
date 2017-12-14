import lzo
import os
import errno
try:
	import cPickle as pickle
except ImportError:
	import pickle
import sqlite3 as sql
try:
	import lzma
except ImportError:
	import backports.lzma as lzma
import bz2
from shutil import copyfileobj



def add_data(filepath,data,label):
	if not os.path.isfile(filepath):
		if not os.path.isfile(filepath+'.xz'):
			raise IOError('No file for poplist: '+filepath+' . You should call init_db before adding elements')
		else:
			xz_decompress(filepath+'.xz')
	pickled_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
	lz_data = lzo.compress(pickled_data)
	conn = sql.connect(filepath)
	with conn:
		cursor = conn.cursor()
#		cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
#				+"T INT, "\
#				+"Population_object BLOB)")
		cursor.execute("DELETE FROM main_table WHERE T="+str(label))
		cursor.execute("INSERT INTO main_table VALUES (?,?)",(label,sql.Binary(lz_data)))


def read_data(filepath,label=None):
	if not os.path.isfile(filepath):
		if not os.path.isfile(filepath+'.xz'):
			raise IOError('No file for poplist: '+filepath+' . You should call init_db before adding elements')
		else:
			xz_decompress(filepath+'.xz')
	conn = sql.connect(filepath)
	with conn:
		cursor = conn.cursor()
		if label is None:
			cursor.execute('SELECT max(T) FROM main_table')
			max_T = cursor.fetchone()[0]
			label = max_T
		cursor.execute("SELECT Population_object FROM main_table WHERE T=\'"+str(label)+"\'")
		blob = cursor.fetchone()
	if blob is None:
		raise IOError('No row in database ' + str(filepath) + ' for label: '+str(label))
	lz_data = blob[0]
	pickled_data = lzo.decompress(lz_data)
	data = pickle.loads(pickled_data)
	return data

def add_data_conn(cursor,filepath,data,label):
	pickled_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
	lz_data = lzo.compress(pickled_data)
	try:
		os.makedirs(os.path.dirname(filepath))
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(filepath)):
			pass
		else:
			raise
	cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
				+"T INT, "\
				+"Population_object BLOB)")
	cursor.execute("INSERT INTO main_table VALUES (?,?)",(label,sql.Binary(lz_data)))

def init_db(filepath):
	try:
		os.makedirs(os.path.dirname(filepath))
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(filepath)):
			pass
		else:
			raise
	conn = sql.connect(filepath)
	with conn:
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
				+"T INT, "\
				+"Population_object BLOB)")

def read_data_conn(cursor,filepath,label=None):
	if not os.path.isfile(filepath):#
		xz_decompress(filepath+'.xz')
		os.remove(filepath+'.xz')
	if label is None:
		cursor.execute('SELECT max(T) FROM main_table')
		max_T = cursor.fetchone()[0]
		label = max_T
	cursor.execute("SELECT Population_object FROM main_table WHERE T=\'"+str(label)+"\'")
	blob = cursor.fetchone()
	lz_data = blob[0]
	pickled_data = lzo.decompress(lz_data)
	data = pickle.loads(pickled_data)
	return data


def xz_decompress(file):
	outfile = file[:-3]
	with open(outfile,'wb') as output:
		with lzma.LZMAFile(file,'rb') as uncompressed:
		#with bz2.BZ2File(file) as uncompressed:
			copyfileobj(uncompressed,output)

def xz_compress(file,rm=False):
	outfile = file+'.xz'
	#with open(outfile) as output:
	with open(file,'rb') as uncompressed:
		with lzma.LZMAFile(outfile,'wb') as compressed:
		#with bz2.BZ2File(outfile,'w') as compressed:
			copyfileobj(uncompressed,compressed)
	if rm:
		os.remove(file)
