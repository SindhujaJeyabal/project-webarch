import urllib2
import json

GIFY_URL = "http://api.giphy.com/"
GIFY_KEY = "dc6zaTOxFJmzC"

def top_gifs(artist_name):
	artist_name=artist_name.replace(' ', '%20')
	print "in gify"
	print artist_name
	
	req_url = GIFY_URL+"v1/gifs/search?q="+artist_name+"&api_key="+GIFY_KEY
	#print req_url

	response = json.loads(urllib2.urlopen(req_url).read())
	#print response
	# print response['data'][0]['images']['original']['url']

	return response['data']