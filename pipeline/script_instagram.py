import pdb
import json, urllib2

def query_instagram_location():
	query_loc_id = 'https://api.instagram.com/v1/locations/search?lat=37.788900&lng=-122.3981040&client_id=f936a78d343c4f758fbb54a4ec51eb20'
	loc_obj = json.load(urllib2.urlopen(query_loc_id))
	pdb.set_trace()
	uid = 235311017
	query = 'https://api.instagram.com/v1/locations/' + str(uid) + '/media/recent?client_id=f936a78d343c4f758fbb54a4ec51eb20'
	media_obj = json.load(urllib2.urlopen(query))
query_instagram_location()