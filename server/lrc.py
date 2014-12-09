import urllib2
import json
# Read lyrics from a url
def readLyrics():
	response = urllib2.urlopen('http://people.ischool.berkeley.edu/~sindhuja/song.lrc')
	lyrics = response.read()
	return lyrics

RESPONSE_FORMAT = "json"

MM_KEY = "1ae163cbc0f747a01f5a396acc059197"
MM_URL = "http://api.musixmatch.com/ws/1.1/"

#top artists
def top_artists():
	req_url = MM_URL + "chart.artists.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&page=1&page_size=10"
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	artists = json_resp['message']['body']['artist_list']	
	return artists

def artist_albums(artist_id):
	req_url = MM_URL + "artist.albums.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&artist_id=" + str(artist_id) + "&s_release_date=desc&g_album_name=1&page=1&page_size=5"
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	albums = json_resp['message']['body']['album_list']
	# print albums
	return albums

def album_tracks(album_id):
	print album_id
	req_url = MM_URL + "album.tracks.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&album_id=" + str(album_id) + "&page=1&page_size=2"
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	#print json_resp
	tracks = json_resp['message']['body']['track_list']
	return tracks

# Get albums and then get tracks from albums
# TODO: figure out duplication while appending multiple album results
def top_tracks(artist_id):
	album_list = artist_albums(artist_id)
	track_list = list()
	for album in album_list:
	# album = album_list[0]
		track_list.extend(album_tracks(album['album']['album_id']))	
	return track_list

def track_lyrics(track_id):
	req_url = MM_URL + "track.lyrics.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&track_id=" + str(track_id)
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	lyrics = json_resp['message']['body']['lyrics']['lyrics_body']	
	return lyrics

# For potential search functionality
def track_search(artist_name, track_name):
	artist_name.replace(' ', '%20')
	track_name.replace(' ', '%20')
	req_url = MM_URL + "track.search?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&q_track=" + track_name + "&q_artist=" + artist_name +"&f_has_lyrics=1&page_size=1"
	response  = urllib2.urlopen(req_url)
	tracks = response.read()
	print tracks
	return tracks

################################     ECHONEST ##########################################

# ECHONEST_URL = "http://developer.echonest.com/api/v4/"
# ECHONEST_API_KEY = "RTHOBAZ2BBKVRTMKE"

# #find top artists on Echonest
# def top_artists():
# 	req_url = ECHONEST_URL + "artist/top_hottt?api_key=" + ECHONEST_API_KEY + "&format=" + RESPONSE_FORMAT + "&results=10"
# 	response  = urllib2.urlopen(req_url)
# 	artists = response.read()
# 	return artists
# # Lookup tracks on echonest

# def artist_songs(artist_id):
# 	req_url = ECHONEST_URL + "artist/songs?api_key=" + ECHONEST_API_KEY + "&id=" + artist_id + "&format=" + RESPONSE_FORMAT +\
# 	"&start=0&results=10"
# 	response  = urllib2.urlopen(req_url)
# 	songs = response.read()
# 	print songs
# 	return songs

# def lookuptracks(artist_id):
# 	pass
# 	# song/search?api_key=FILDTEOIK2HBORODV&format=json&artist=radiohead&title=creep&bucket=id:lyricfind-US&limit=true&bucket=tracks
