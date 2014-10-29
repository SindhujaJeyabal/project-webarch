import sqlite3
from flask import g

# Helper function to check if a short url exists in db.
def checkifexists(ip_shorturl):
	conn = sqlite3.connect("dbase/shorten.db")
	c = conn.cursor()
	query='select * from urls where shorturl = ?'
	c.execute(query, ip_shorturl)
	if len(c.fetchall()):
		return True
	return False

# Helper function without dbopen and close
def ifexists(conn,ip_shorturl):
	print "ipurl:", ip_shorturl, len(ip_shorturl)
	query='select longurl from urls where shorturl = ?'
	tup = [(ip_shorturl)]
	conn.execute(query, tup)
	if len(conn.fetchall()):
		return True
	return False

# Add a new short,long url pair to db
def addurltodb(ip_shorturl, longurl):
	conn = sqlite3.connect("dbase/shorten.db")
	c = conn.cursor()
	if ifexists(c,ip_shorturl):
		return False

	objtoadd = (ip_shorturl, longurl)
	query='insert into urls values (?,?)'
	c.execute(query,objtoadd)
	
	conn.commit()
	conn.close()
	return True

# retrieve long url from db for redirect purposes
def getlongurlfromdb(ip_shorturl):
	conn = sqlite3.connect("dbase/shorten.db")
	c = conn.cursor()
	query='select longurl from urls where shorturl = ?'
	tup = [(ip_shorturl)]
	c.execute(query, tup)
	result = c.fetchall()
	print result
	if len(result) != 1:
		print "PANIC"
		return ''
	return result[0][0]



