#-*- coding: utf-8 -*-
import sys, os, time
reload(sys)
sys.setdefaultencoding('utf-8')

import subprocess

def gradeScore(code):
	foldername = str(time.time())
	subprocess.call(["cp","MazeRunner",foldername,'-r'])
	f = open(foldername+'/myMazeAlgo.cpp', 'w')
	code = code.split('\r\n')
	for i in code:
		f.write(i+'\n')
	f.close()
	time.sleep(0.1)
	subprocess.call(["g++",foldername+'/main.cpp','-o',foldername+'/program'])
	time.sleep(0.1)
	return subprocess.check_output(foldername+'/program',shell=True)