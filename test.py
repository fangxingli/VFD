#!/usr/bin/python
import util

def f():
	raise util.NetworkError('asdf')
	print '2133333333333333333333333333'

def g():
	f()
	print 'after f()'

def a():
	g()
	print 'after g()'

try:
	a()
except util.MPException,e:
	print e
