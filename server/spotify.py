import urllib2
import json

def get_song(spotify_id):
	
	req_url = "https://api.spotify.com/v1/tracks/"+spotify_id

	response = urllib2.urlopen(req_url)
	song = json.loads(response.read())

	return song['preview_url']