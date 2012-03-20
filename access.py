#!/usr/bin/python
import os, sys
#v0_1

NAME='pptv'

if __name__ == '__main__':
	target_dir = os.getcwd() + '/' + sys.argv[1][:2] + '/'
	target_files = [ target_dir+'default_'+sys.argv[1] + '.py', target_dir+'phony_'+sys.argv[1] + '.py']
	for i in target_files:
		if i.find('default') != -1:
			os.system('cp %s /home/ftp/%s.py' %(i, NAME))
		else:
			os.system('cp %s /home/ftp/phony.py' %(i))
	os.chdir('/home/ftp')
	os.system('tar zcvf %s.tgz phony.py %s.py' % (NAME, NAME))
