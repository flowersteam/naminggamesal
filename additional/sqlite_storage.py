import lzo
import os
import errno
import cPickle
import sqlite3 as sql
import backports.lzma as lzma
import bz2
from shutil import copyfileobj



def add_data(filepath,data,label,priority='decompressed'):
	if priority == 'compressed' and os.path.isfile(filepath+'.xz'):
		xz_decompress(filepath+'.xz')
	pickled_data = cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL)
	lz_data = lzo.compress(pickled_data)
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
		cursor.execute("INSERT INTO main_table VALUES (?,?)",(label,sql.Binary(lz_data)))


def read_data(filepath,label=None,priority='decompressed'):
	if not os.path.isfile(filepath) or (priority == 'compressed' and os.path.isfile(filepath+'.xz')):
		xz_decompress(filepath+'.xz')
		#os.remove(filepath+'.xz')
	conn = sql.connect(filepath)
	with conn:
		cursor = conn.cursor()
		if label is None:
			cursor.execute('SELECT max(T) FROM main_table')
			max_T = cursor.fetchone()[0]
			label = max_T
		cursor.execute("SELECT Population_object FROM main_table WHERE T=\'"+str(label)+"\'")
		blob = cursor.fetchone()
	lz_data = blob[0]
	pickled_data = lzo.decompress(lz_data)
	data = cPickle.loads(pickled_data)
	return data

def add_data_conn(cursor,filepath,data,label):
	pickled_data = cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL)
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
	data = cPickle.loads(pickled_data)
	return data


def xz_decompress(file):
	outfile = file[:-3]
	with open(outfile,'w') as output:
		with lzma.LZMAFile(file) as uncompressed:
		#with bz2.BZ2File(file) as uncompressed:
			copyfileobj(uncompressed,output)

def xz_compress(file,rm=False):
	outfile = file+'.xz'
	#with open(outfile) as output:
	with open(file) as uncompressed:
		with lzma.LZMAFile(outfile,'w') as compressed:
		#with bz2.BZ2File(outfile,'w') as compressed:
			copyfileobj(uncompressed,compressed)
	if rm:
		os.remove(file)
