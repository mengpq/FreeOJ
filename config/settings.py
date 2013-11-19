#!/usr/bin/env python
# coding: utf-8
import web

db = web.database(dbn = 'mysql', db = 'FreeOJ', user = '', pw = '')
render = web.template.render('templates/', cache = False)

config = web.storage(
    email = 'mengpq@gmail.com',
	author = 'AcFast',
    site_name = 'FreeOJ',
    site_desc = '',
    static = '/static',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
