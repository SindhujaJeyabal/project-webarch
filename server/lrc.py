import urllib2

# Read lyrics from a url
def readLyrics():
	response = urllib2.urlopen('http://people.ischool.berkeley.edu/~sindhuja/song.lrc')
	lyrics = response.read()
	return lyrics

ECHONEST_URL = "http://developer.echonest.com/api/v4/"
ECHONEST_API_KEY = "RTHOBAZ2BBKVRTMKE"
ECHONEST_RESPONSE_FORMAT = "json"

#find top artists on Echonest
def top_artists():
	req_url = ECHONEST_URL + "artist/top_hottt?api_key=" + ECHONEST_API_KEY + "&format=" + ECHONEST_RESPONSE_FORMAT + "&results=10"
	response  = urllib2.urlopen(req_url)
	artists = response.read()
	return artists
# Lookup tracks on echonest

def artist_songs(artist_id):
	req_url = ECHONEST_URL + "artist/songs?api_key=" + ECHONEST_API_KEY + "&id=" + artist_id + "&format=" + ECHONEST_RESPONSE_FORMAT +\
	"&start=0&results=10"
	response  = urllib2.urlopen(req_url)
	songs = response.read()
	print songs
	return songs

def lookuptracks(artist_id):
	pass
	# song/search?api_key=FILDTEOIK2HBORODV&format=json&artist=radiohead&title=creep&bucket=id:lyricfind-US&limit=true&bucket=tracks