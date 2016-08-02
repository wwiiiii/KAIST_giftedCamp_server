#-*- coding: utf-8 -*-
import sys, os, time
reload(sys)
sys.setdefaultencoding('utf-8')

import subprocess

MAP_NUM = 2

def gradeScore(code):
	foldername = 'folders/' + str(time.time())
	subprocess.call(["cp","MazeRunner",foldername,'-r'])
	f = open(foldername+'/myMazeAlgo.cpp', 'w')
	code = code.split('\r\n')
	for i in code:
		f.write(i+'\n')
	f.close()
	time.sleep(0.1)
	subprocess.call(["g++",foldername+'/main.cpp','-o',foldername+'/program'])
	time.sleep(0.1)
	res = ""
	for i in range(1,MAP_NUM+1):
		nowres = subprocess.check_output(foldername+'/program '+'/home/ubuntu/KAIST_giftedCamp_server/maps/map'+str(i)+'.txt',shell=True)
		if nowres.find('Clear') != -1:
			nowres = nowres[res.find('Clear'):]
		elif nowres.find('Fail') != -1:
			nowres = nowres[res.find('Fail'):]
		elif nowres.find('Error') != -1:
			nowres = nowres[res.find('Error'):]
		res += nowres + '\n'
		print nowres
	return res