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

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
def landing_page():
	return flask.render_template(
            'home.html')

@app.errorhandler(404)
def page_not_found(e):
	return flask.render_template('output.html', prefix = "URL not found", url=''), 404

@app.route('/server/shorts/<short_url>')
def shorts_get(short_url):
	destination = getlongurlfromdb(short_url)
	if destination == '':
		print "URL not found"
		abort(404)
		# return flask.render_template('output.html', prefix = "URL not found", url='')
	return flask.redirect(destination)

@app.route('/server/shorts', methods=['PUT', 'POST'])
def shorts_put():
	long_url=request.form.get('longURL')
	short_url=request.form.get('shortURL')
	shortened_url="http://127.0.0.1:5000/server/shorts/"+short_url
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
            url=shortened_url)


if __name__ == "__main__":
    app.run()#port=int(environ['FLASK_PORT']))
