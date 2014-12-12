import urllib2
import json

def main():
	giphy_url="http://api.giphy.com/v1/gifs/search?q=funny+cat&api_key=dc6zaTOxFJmzC"
	results = urllib2.urlopen(giphy_url)
	json_data =json.load(results)

	print json_data["data"][0]["images"]["original"]["url"]

if __name__=="__main__":
	main()

