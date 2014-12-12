import urllib2
import json

GIFY_URL = "http://api.giphy.com/"
GIFY_KEY = "dc6zaTOxFJmzC"

def top_gifs(artist_name):
	artist_name_rep=artist_name.replace(' ', '%20')
	print "in gify"
	print artist_name_rep
	
	req_url = GIFY_URL+"v1/gifs/search?q="+artist_name_rep+"&api_key="+GIFY_KEY
	#print req_url

	response = json.loads(urllib2.urlopen(req_url).read())
	gif_list = response['data']
	if len(gif_list) < 5:
		artist_list = artist_name.split(' ')
		if artist_list[0] != artist_name:
			req_url = GIFY_URL+"v1/gifs/search?q="+artist_list[0]+"&api_key="+GIFY_KEY
			response = json.loads(urllib2.urlopen(req_url).read())
			gif_list.extend(response['data'])

	if len(gif_list) < 5:
		req_url = GIFY_URL+"v1/gifs/search?q=doge&api_key="+GIFY_KEY
		response = json.loads(urllib2.urlopen(req_url).read())
		gif_list.extend(response['data'])

	return gif_list