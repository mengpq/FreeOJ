#!/usr/bin/env python
# coding: utf-8

prefix = 'process.'

urls = (
    '/',                	prefix + 'main.index',
	'/status',				prefix + 'main.status',
	'/problem',				prefix + 'main.problemset',
	'/problem/(\d+)',		prefix + 'main.problem',
	'/register',			prefix + 'main.register',
	'/login',				prefix + 'main.login',
	'/logout',				prefix + 'main.logout',
	'/profile',				prefix + 'main.profile',
	'/submit',				prefix + 'main.submit',
)

