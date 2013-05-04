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

	def create_problem_table(self):
		problem_table = """(
		pid int NOT NULL AUTO_INCREMENT,
		title varchar(80),
		tag varchar(1024),
		source varchar(128) NOT NULL,
		sourceid varchar(64) NOT NULL,
		PRIMARY KEY (pid)
		) AUTO_INCREMENT = 1000
		"""
		self.cursor = self.conn.cursor()
		print ("create table if not exists problem %s" % problem_table)
		self.cursor.execute("create table if not exists problem %s" % problem_table)
	
	def create_status_table(self):
		status_table ="""(
		runid INT NOT NULL AUTO_INCREMENT,
		handle VARCHAR(255) NOT NULL,
		problemid INT NOT NULL,
		result varchar(64),
		ispending int,
		memory INT,
		runtime INT,
		language VARCHAR(64) NOT NULL,
		codelen INT,
		submittime VARCHAR(32),
		sourcecode TEXT,
		status_hash varchar(128),
		PRIMARY KEY (runid)
		) AUTO_INCREMENT = 1
		"""
		self.cursor = self.conn.cursor()
		print ("create table if not exists status %s" % status_table)
		self.cursor.execute("create table if not exists status %s" % status_table)

host = 'localhost'
user = 'root'
passwd = 'mpqisacfast'
dbname = 'FreeOJ'

db = dbinit(host,user,passwd,dbname)
db.create_status_table()
