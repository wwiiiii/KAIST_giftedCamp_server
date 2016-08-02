#-*- coding: utf-8 -*-
import sys, os, time
reload(sys)
sys.setdefaultencoding('utf-8')

import subprocess

MAP_NUM = 9
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
	res = ""; sum = 0
	for i in range(1,MAP_NUM+1):
		p = subprocess.Popen([foldername+'/program' , mapPath+str(i)+'.txt' , foldername+'/result'+str(i)])
		time.sleep(0.1)
		p.terminate()
		if os.path.exists(foldername+'/result'+str(i)):
			nowres = open(foldername+'/result'+str(i), 'r').readlines();
			print nowres
			nowres=  str(nowres[0]); print nowres
			res += str(i)+'th ' + nowres
			if nowres.find('Clear') != -1:
				sum += int(nowres[nowres.find('Move Count : ')+len('Move Count : '):])
		else:
			nowres = str(i)+'th TimeOut\n'
			res += str(i)+'th TimeOut\n'
		print nowres
	return res + 'Total Move Count is ' + str(sum)