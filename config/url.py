#!/usr/bin/env python
# coding: utf-8

prefix = 'process.'

urls = (
    '/',                    prefix + 'main.index',
	'/status/.*',			prefix + 'main.status',
	'/problem/.*',			prefix + 'main.problem',
	'/register/.*',			prefix + 'main.register',
	'/login/.*',			prefix + 'main.login',
	'/submit/.*',			prefix + 'main.submit',
)

