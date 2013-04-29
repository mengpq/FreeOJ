#!/usr/bin/env python
# coding: utf-8

from config.url import urls
import web

app = web.application(urls, globals())

def notfound():
	render = web.template.render("templates")
	return web.notfound(render.notfound())

if __name__ == "__main__":
	app.notfound = notfound
	app.run()
