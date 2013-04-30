#!/usr/bin/env python
# coding: utf-8
import web, re, hashlib
from config import settings
from datetime import datetime

render = settings.render
db = settings.db

class index:
	def GET(self):
		return render.index()

class status:
	def GET(self):
		return render.status(1)

class problem:
	def GET(self):
		return render.problem()

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
		raise web.seeother("/")

class login(secure):
	
	def error_login_msg(self, msg, data):
		return render.login(msg,data)

	def GET(self):
		return render.login()

	def POST(self):
		data = web.input(login_handle = None, login_password = None)
		if data.login_handle == None: return render.login()
		msg = secure.check_login(self,data.login_handle, data.login_password)
		if msg != 'success':
			return self.error_login_msg(msg,data)
		raise web.seeother("/")

class submit:
	def GET(self):
		return render.submit('hello world')
