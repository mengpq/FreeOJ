#!/usr/bin/env python
# coding: utf-8
import web

render = web.template.render('templates/', cache=False)

web.config.debug = True

config = web.storage(
    email = 'mengpq@gmail.com',
	author = 'AcFast',
    site_name = 'FreeOJ',
    site_desc = '',
    static = '/static',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

