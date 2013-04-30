import MySQLdb

class dbinit():
	def __init__(self, host, user, passwd, dbname, port = 3306):
		self.conn = MySQLdb.connect(host,user,passwd,port = port)
		self.cursor = self.conn.cursor()
		self.cursor.execute("create database if not exists %s" % dbname)
		self.conn.select_db(dbname)

	def create_user_table(self):
		user_table = """(
		handle varchar(255) NOT NULL,
		password varchar(255) NOT NULL,
		email varchar(255),
		reg_date varchar(32),
		type int
		)
		"""
		self.cursor = self.conn.cursor()
		print ("create table if not exists user %s" % user_table)
		self.cursor.execute("create table if not exists user %s" % user_table)


host = 'localhost'
user = 'root'
passwd = 'mpqisacfast'
dbname = 'FreeOJ'

db = dbinit(host,user,passwd,dbname)
db.create_user_table()
