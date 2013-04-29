#!/usr/bin/env python
# coding: utf-8
import web
from config import settings
from datetime import datetime

render = settings.render

class index:
	def GET(self):
		return render.index()

class status:
	def GET(self):
		return render.status(1)

class problem:
	def GET(self):
		return render.problem()

class register:
	def GET(self):
		return render.register()

class login:
	def GET(self):
		return render.login()
