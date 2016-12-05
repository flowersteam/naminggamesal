import lzo


import sqlite3 as sql





def add_data(filepath,data,label):
	lz_data = lzo.compress(data)
	conn = sql.connect(filepath)
	with conn:
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS main_table("\
				+"T INT, "\
				+"Population_object BLOB)")
		cursor.execute("INSERT INTO main_table VALUES (?,?)",(label,sql.binary(lz_data)))

def read_data(filepath,label=None):
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
	return lzo.decompress(lz_data)
