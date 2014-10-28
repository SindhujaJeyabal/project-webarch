#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ
import sqlite3
from contextlib import closing
from db import *

app = flask.Flask(__name__)
app.debug = True

@app.route('/server/shorts', method=['GET'])
def shorts_get():
	shortened_url = request.form.get('shortened_url')
	destination = getlongurlfromdb(shortened_url)
	return flask.redirect(destination)

@app.route('/server/shorts', method=['PUT', 'POST'])
def shorts_put():
	long_url=request.form.get('long_url')
	short_url=request.form.get('short_url')
	shortened_url="http://people.ischool.berkeley.edu/~anubhav.gupta/server/shorts/"+short_url
	addurltodb(shortened_url, long_url)
	return "Generated new short url -->" shortened_url

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
