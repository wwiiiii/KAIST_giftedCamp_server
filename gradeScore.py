#-*- coding: utf-8 -*-
import sys, os, time
reload(sys)
sys.setdefaultencoding('utf-8')

import subprocess

MAP_NUM = 2
mapPath = '/home/ubuntu/KAIST_giftedCamp_server/maps/map'
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
		subprocess.call([foldername+'/program' , mapPath+str(i)+'.txt' , foldername+'/result'+str(i)])
		time.sleep(0.05)
		if os.path.exists(foldername+'/result'+str(i)):
			nowres = open(foldername+'/result'+str(i), 'r').readlines();
			nowres=  str(nowres[0])
			if nowres.find('Clear') != -1:
				nowres = nowres[res.find('Clear'):]
			elif nowres.find('Fail') != -1:
				nowres = nowres[res.find('Fail'):]
			elif nowres.find('Error') != -1:
				nowres = nowres[res.find('Error'):]
			res += str(i)+'th ' + nowres + '\n'
		else:
			nowres = str(i)+'th Failed\n'
			res += str(i)+'th Failed\n'
		print nowres
	return res