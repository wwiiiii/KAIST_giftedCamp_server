# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, send_file, send_from_directory, redirect, url_for
from werkzeug.wrappers import BaseRequest, BaseResponse
from urlparse import urlparse
import sys, time, io, os
import urllib
import gradeScore

reload(sys)

def uri_validator(x):
	if x.find('myfile:') != -1:
		return True
	try:
		result = urlparse(x)
		if result.scheme!='' and result.netloc!='' and result.path !='': return True
		else: return False
	except:
		return False

UPLOAD_FOLDER ='/home/ubuntu/KAIST_giftedCamp_server/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)#, template_folder = '/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
@app.route('/')
def home():
  return render_template('home.html')
  

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/grade')
def grade():
	return render_template('grade.html')

@app.route('/gradecalc',methods = ['POST'])
def gradecalc():
	print request
	if request.method != 'POST':
		return 'Access Denied'
	print request.form
	code= request.form['code'];
	foldername = str(time.time())
	return str(gradeScore.gradeScore(code))

if __name__ == "__main__":
	if len(sys.argv) == 1:
		myport = 12345
	else:
		myport = int(sys.argv[1])
	print 'asdf'
	app.run(host='0.0.0.0', port=myport)
	
	
	
