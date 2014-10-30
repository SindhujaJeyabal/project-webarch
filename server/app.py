#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ
import sqlite3
from contextlib import closing
from db import *
from jinja2 import TemplateNotFound
from flask import abort
import time
import math

app = flask.Flask(__name__)
app.debug = True
ROOT_URL = "http://people.ischool.berkeley.edu/~carlos/project-webarch/server/shorts/"

def get_url_from_timestamp():
	tt = int(time.time())
	digits = []
	while tt > 0:
  		remainder = tt % 52
  		digits.append(remainder)
  		tt = tt / 52
  	print digits
	digits.reverse()
	print "after rev:", digits
	letters = []
	for d in digits:
		ascii_code = ''
		if d > 26:
			ascii_code = 65 + (d-26)
		else:
			ascii_code = 97 + d
		letters.append(str(unichr(ascii_code)))

	surl = ''.join(letters)
	print surl
	return surl

@app.route('/')
def landing_page():
	return flask.render_template(
            'home.html')

@app.errorhandler(404)
def page_not_found(e):
	return flask.render_template('404.html', prefix = "URL not found", url=''), 404

@app.route('/server/shorts/<short_url>')
def shorts_get(short_url):
	destination = getlongurlfromdb(short_url)
	print 'longURL: ', destination
	if destination == '':
		print "URL not found"
		abort(404)
		return
		# return flask.render_template('output.html', prefix = "URL not found", url='')
	if not (destination.startswith('http://') or destination.startswith('https://')):
		destination = 'http://' + destination
	return flask.redirect(destination)

@app.route('/server/shorts', methods=['PUT', 'POST'])
def shorts_put():
	long_url=request.form.get('longURL')
	short_url=request.form.get('shortURL')
	if short_url == '':
		db_entries = getallentries(long_url)
		db_entries = [ROOT_URL + url for url in db_entries]

		if len(db_entries) == 0:
			short_url = get_url_from_timestamp()
		else:
			prefix = "URL pair is already matched"
			return flask.render_template(
            'output.html', prefix = prefix,
            urllist= db_entries)

	shortened_url = ROOT_URL + short_url
	ret_type = addurltodb(short_url, long_url)
	prefix = ''
	if ret_type:
		prefix = "Your new url is:"
	else:
		db_long_url = getlongurlfromdb(short_url)
		print "db_long_url: ", db_long_url
		if db_long_url == long_url:
			prefix = "URL pair is already matched"
		else:
			prefix = "URL is already taken."
			shortened_url = ''
	return flask.render_template(
            'output.html', prefix = prefix,
            urllist=shortened_url.split())


if __name__ == "__main__":
    app.run()#port=int(environ['FLASK_PORT']))
