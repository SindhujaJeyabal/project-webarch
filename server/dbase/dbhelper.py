import sqlite3
from flask import g

def create_url_table():
	conn = sqlite3.connect("shorten.db")
	c = conn.cursor()
	
	querytoExec="create table urls (shorturl text not null, longurl text not null);"
	c.execute(querytoExec)
	conn.commit()
	conn.close()

if __name__ == '__main__':
	create_url_table()
