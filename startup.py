#!/usr/bin/env python
# coding: utf-8

from config.url import urls
import web

web.config.debug = False
app = web.application(urls, globals())
web.config.session_parameters['timeout'] = 10
session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'handle':"",'logined':False})
web.template.Template.globals['session'] = session 

def session_hook():
	web.ctx.session = session

def notfound():
	render = web.template.render("templates")
	return web.notfound(render.notfound())

app.add_processor(web.loadhook(session_hook))

if __name__ == "__main__":
	app.notfound = notfound
	app.run()
