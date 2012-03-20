#!/usr/bin/env python
__applicationName__ = "codemanage" 
__doc__ = """
Personal code management
"""
__author__ = "Fangxing Li"
__date__ = "2012/03/20"
"""
	param: add remove push	
"""

import os, sys

CWD = os.getcwd()
PACKAGE_PATH = CWD + '/package'

def pathFormat(path):
	code_name = ''
	code_dir = ''
	tmp_path = ''
	if os.path.isdir(path):
		if path[-1] == '/':
			tmp_path = path[:-1]
	else:
		tmp_path = path

	code_name = tmp_path.split('/')[-1]
	code_dir = tmp_path.replace(code_name, '')
	return code_dir, code_name	

if __name__ == "__main__":
	if os.path.exists(PACKAGE_PATH) == False:
		print 'cm_shell=> package does not exists'

	if sys.argv[1] == 'add':
		if os.path.exists(PACKAGE_PATH + sys.argv[2]):
			print 'cm_shell=> code %s exists, do you want to recover it?[Yes]' % sys.argv[2]
			getin = open('/proc/self/fd/0', 'r').readline().strip()
			if getin.lower() == 'n':
				print 'cm_shell=> cm exit'
				exit(0)
			os.system('rm %s -r' %(PACKAGE_PATH + sys.argv[2]))
			os.system('cp %s %s' %(sys.argv[2], PACKAGE_PATH))
