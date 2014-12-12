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
import lrc
import string
import json
import gify
import sc

app = flask.Flask(__name__)
app.debug = True
SHORT_ROOT_URL = "http://people.ischool.berkeley.edu/~ssnipes/server/shorts/"
#SHORT_ROOT_URL = "http://127.0.0.1:5000/"

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

@app.route('/demo.html')
def showLyrics():
	lyrics = lrc.readLyrics()
	all_lines = lyrics.split('\n')
	time_words = []
	for line in all_lines:
		items = line.strip(string.punctuation).split(']')
		if len(items) > 1:
			time_words.append((items[0],items[1].strip('\r')))
	gifs = load_gifys("One%20Direction")
	return flask.render_template('audio.html', lyrics=json.dumps(time_words), gifs = gifs)

@app.route('/artists.html')
def mm_topartists():
	# artists = lrc.top_artists()   
	artists = lrc.artist_search()
	return flask.render_template('test_page.html', subheader_val='0', track_id='0', artists = artists, gifs=list(), soundcloud_id='-1')

@app.route('/tracks.html/<artist_id>/<artist_name>')
def mm_toptracks(artist_id, artist_name):
	tracks = lrc.top_tracks(artist_id)
	return flask.render_template('test_page.html', subheader_val='1', track_id='0', artist_name = artist_name, gifs = list(), tracks = tracks, soundcloud_id='-1')

def load_gifys(artist_name):
	gifs = gify.top_gifs(artist_name)
	urllist = list()
	for i in range(len(gifs)):
		urllist.append(gifs[i]['images']['original']['url'].encode('utf-8','ignore'))
	# print urllist[0]
	return urllist

@app.route('/track.html/<track_id>/<artist_name>/<track_name>/<soundcloud_id>')
def mm_tracklyrics(track_id, artist_name, track_name, soundcloud_id):
	print track_name
	track_name = track_name.split('(', 1)[0]
	print track_name
	lyrics = lrc.track_lyrics(track_id)
	gifs = load_gifys(artist_name)
	print "########### sound cloud id is ##########", soundcloud_id
	return flask.render_template('test_page.html', subheader_val='2', artist_name = artist_name, track_id=track_id, lyrics = lyrics, gifs = gifs, track_name=track_name, soundcloud_id = soundcloud_id)

@app.route('/share.html/<track_id>/<artist_name>/<track_name>/<soundcloud_id>')
def shorts_put(track_id,artist_name, track_name, soundcloud_id):
	#artist_name=artist_name.replace(' ', '%20')
	#track_name=track_name.replace(' ', '%20')
	long_url="http://people.ischool.berkeley.edu/~ssnipes/server/track.html/"+track_id+"/"+artist_name+"/"+track_name+"/"+soundcloud_id
	print long_url
	short_url=get_url_from_timestamp()
	print short_url

	shortened_url = SHORT_ROOT_URL + short_url
	print shortened_url
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

@app.route('/shorts/<short_url>')
def shorts_get(short_url):
	short_url=short_url.replace(' ', '%20')
	print short_url
	destination = getlongurlfromdb(short_url)
	print 'longURL: ', destination
	if destination == '':
		print "URL not found"
		abort(404)
		return
	if not (destination.startswith('http://') or destination.startswith('https://')):
		destination = 'http://' + destination
	return flask.redirect(destination)

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
