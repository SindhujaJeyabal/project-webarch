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

def artist_albums(artist_id, page_num=1):
	req_url = MM_URL + "artist.albums.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&artist_id=" + str(artist_id) + "&s_release_date=desc&g_album_name=1&page=" + str(page_num) + "&page_size=10"
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	albums = json_resp['message']['body']['album_list']
	available_num = json_resp['message']['header']['available']
	#print albums
	return albums, available_num

def album_tracks(album_id):
	print album_id
	req_url = MM_URL + "album.tracks.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&album_id=" + str(album_id) # + "&page=1&page_size=50"
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	#print json_resp
	tracks = json_resp['message']['body']['track_list']
	available_num = json_resp['message']['header']['available']
	return tracks, available_num

# Get albums and then get tracks from albums
# TODO: figure out duplication while appending multiple album results
def already_present(tracks, track_name):
	# bool_flags = [track_name == track['track']['track_name'] for track in tracks]
	# b_result = True
	# for b in bool_flags:
	# 	b_result = b or b_result
	# return b_result
	hit = 0
	for track in tracks:
		if track['track']['track_name'] == track_name:
			hit = 1
			break
	return (hit == 1)

def top_tracks(artist_id):
	page_num = 1
	track_list = list()
	# while 1:
	album_list, avbl_albums = artist_albums(artist_id)
	for album in album_list:
	# album = album_list[0]
		tracks, avbl_tracks = album_tracks(album['album']['album_id'])
		#print tracks
		for track in tracks:
			#print track
			if not already_present(track_list, track['track']['track_name']): #track['track']['track_soundcloud_id'] != 0 and 
				track_list.append(track)
			if len(track_list) == 10:
				return track_list
		# page_num += 1
		# print page_num
		# if page_num > 5:
		# 	break
	print track_list	
	return track_list

def track_lyrics(track_id):
	req_url = MM_URL + "track.lyrics.get?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&track_id=" + str(track_id)
	json_resp = json.loads(urllib2.urlopen(req_url).read())
	lyrics = json_resp['message']['body']['lyrics']['lyrics_body']
	ly_list = lyrics.split('\n')
	return ly_list

# For potential search functionality
def track_search(artist_name, track_name):
	artist_name.replace(' ', '%20')
	track_name.replace(' ', '%20')
	req_url = MM_URL + "track.search?apikey=" + MM_KEY + "&format=" + RESPONSE_FORMAT + \
	"&q_track=" + track_name + "&q_artist=" + artist_name +"&f_has_lyrics=1&page_size=1"
	response  = urllib2.urlopen(req_url)
	tracks = json.loads(response.read())
	#print len(tracks['message']['body']['track_list'])
	# for i in range(len(tracks['message']['body']['track_list'])):
	# 	if (tracks['message']['body']['track_list'][i]['track']['track_soundcloud_id'] != 0):
	# 		return tracks['message']['body']['track_list'][i]['track']
	#print tracks['message']['body']['track_list'][0]['track']
	return tracks['message']['body']['track_list'][0]['track']

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
