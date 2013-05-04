#!/usr/bin/env python
# coding: utf-8
import web, re, hashlib, thread, time
import submitor
from config import settings
from datetime import datetime

db = settings.db
render = settings.render

def user_login(handle):
	web.ctx.session.handle = handle
	web.ctx.session.logined = True

def submitcode_thread(data, handle, status_hash):
	if data.orginal_oj == "codeforces":
		robot = submitor.codeforces()
		robot.submit(data.language, data.source_id, data.source_code)
		total = 0
		while total < 120:
			time.sleep(1)
			res = robot.get_result()
			if res['source_id'] != data.source_id: continue
			db.update('status', where = "status_hash = '" + str(status_hash) + "'", result = res['result'], memory = res['memory'], runtime = res['runtime'])
			if not re.search('ing',res['result']): 
				db.update('status', where = "status_hash ='" + str(status_hash) + "'", ispending = 0)
				break
			total += 1

def submitcode(data):
	nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	status_hash = hashlib.sha1(str(datetime.now()) + str(web.ctx.session.handle) + str(data.problem_id)).hexdigest()
	db.insert('status',handle = web.ctx.session.handle, problemid = data.problem_id, result = 'pending', ispending=1, memory = 0, runtime = 0, language = data.language, codelen = len(data.source_code), submittime = nowtime, sourcecode = data.source_code, status_hash = status_hash)
	thread.start_new_thread(submitcode_thread,(data,web.ctx.session.handle,status_hash))

class index:
	def GET(self):
		return render.index()

class status:

	def GET(self):
		if not web.ctx.session.logined:
			raise web.seeother("/login")
		result = db.select('status', order = 'runid desc')
		return render.status(result)

class problemset:

	def GET(self):
		if not web.ctx.session.logined:
			raise web.seeother("/login")
		result = db.select('problem')
		return render.problemset(result)

class problem:
	def GET(self,problemid):
		if not web.ctx.session.logined:
			raise web.seeother('/login')
		q = db.select('problem',where = 'pid = ' + str(problemid))
		if not q:
			raise web.seeother('/problem')
		result = q[0]
		f = open('./static/codeforces/' + result.sourceid + '.html')
		return render.problem(result,f.read())

class secure:
	def empty(self, string):
		return string == None or len(string) == 0
	
	def check_charset(self, pattern, string):
		result = re.findall(pattern, string)
		return not (result == None or len(result[0]) != len(string))

	def is_handle_exists(self, handle):
		if not handle: return False
		result = db.select('user', where = "handle='" + handle +"'")
		if not result:
			return False
		return True

	def check_login(self, handle, password):
		if self.empty(handle) or not self.check_charset('[0-9a-z@_.]+',handle):
			return 'the handle is illegal'
		elif not self.is_handle_exists(handle):
			return 'the handle is not exists'
		else:
			result = db.select('user', where = "handle='" + handle + "'")[0]
			if result.password != hashlib.sha1(password).hexdigest():
				return 'the password is incorrect'
			else:
				return 'success'
	

class register(secure):
	def error_register_msg(self, msg, data):
		return render.register(msg,data)

	def GET(self):
		return render.register()

	def POST(self):
		data = web.input(reg_handle = None, reg_password = None, reg_confirm_password = None, reg_email = None)
		if secure.empty(self,data.reg_handle):
			return self.error_register_msg("the handle can't be empty",data)
		elif not secure.check_charset(self,'[0-9a-z@_.]+',data.reg_handle):
			return self.error_register_msg("the handle must be digit, lowercase,@,_,.",data)
		elif secure.empty(self,data.reg_password) or secure.empty(self,data.reg_confirm_password):
			return self.error_register_msg("the password can't be empty",data)
		elif data.reg_password != data.reg_confirm_password:
			return self.error_register_msg("two password are different",data)
		elif len(data.reg_password) < 6:
			return self.error_register_msg("the len of the password must be not less than 6",data)
		elif secure.is_handle_exists(self,data.reg_handle):
			return self.error_register_msg("the handle has been used, please choose another hadnle",data)
		else:
			data.reg_password = hashlib.sha1(data.reg_password).hexdigest()
			db.insert('user',handle = data.reg_handle, password = data.reg_password, type = 0, reg_date = datetime.now(), email = data.reg_email)
			user_login(data.reg_handle)
		raise web.seeother("/")

class login(secure):
	
	def error_login_msg(self, msg, data):
		return render.login(msg,data)

	def GET(self):
		if web.ctx.session.logined:
			return render.index()
		return render.login()

	def POST(self):
		data = web.input(login_handle = None, login_password = None)
		if data.login_handle == None: return render.login()
		msg = secure.check_login(self,data.login_handle, data.login_password)
		if msg != 'success':
			return self.error_login_msg(msg,data)
		user_login(data.login_handle)
		raise web.seeother("/")

class logout():
	
	def GET(self):
		web.ctx.session.kill()
		raise web.seeother("/")

class profile():

	def GET(self):
		if not web.ctx.session.logined:
			raise web.seeother("/login")
		return render.profile()

	def POST(self):
		if not web.ctx.session.logined:
			raise web.seeother("/login")
		data = web.input(handle = None, password = None, confirm_password = None, email = None)
		if data.handle != web.ctx.session.handle:
			raise web.seeother("/login")
		if data.password:
			if data.password != data.confirm_password:
				return render.profile("two password is different")
			if len(data.password) < 6:
				return render.profile(" the len of the password must be not less than 6")
			db.update('user',where = "handle='" + data.handle + "'",password = hashlib.sha1(data.password).hexdigest())
		if data.email:
			db.update('user',where = "handle='" + data.handle + "'", email = data.email)
		raise web.seeother("/")

class submit:
	def GET(self):
		return render.submit('hello world')

	def POST(self):
		if not web.ctx.session.logined:
			raise web.othersee("/login")
		data = web.input(orginal_oj = None, problem_id = None, source_id = None, source_code = None, language = None)
		submitcode(data)
		raise web.seeother("/status")
