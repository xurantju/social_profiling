import pdb
import json, urllib2


from pipeline import Pipeline, _load_obj

def _get_pipeline(data_source):
	return Pipeline(data_source=data_source)


def single_address_full_pipeline():
	data_source = 'instagram'
	pipeline = _get_pipeline(data_source)

	# step 1: query retsly to get listing geolocation
	coordinates, address, retsly_ids = pipeline.query_retsly_v1()

	# get instgram media data
	#geolocation_tuple = [-122.4120249,37.73691843]
	#current_loc_trulia = [-122.3981040, 37.788900]
	pipeline.query_instagram_media(coordinates)


def sf_batch_full_pipeline():
	data_source = 'instagram'
	pipeline = _get_pipeline(data_source)

	# step 1: query retsly to get listing geolocation
	coordinates, address, retsly_ids = pipeline.query_retsly_v1()
	pdb.set_trace()
	# get instgram media data
	#geolocation_tuple = [-122.4120249,37.73691843]
	#current_loc_trulia = [-122.3981040, 37.788900]
	try:

	pipeline.query_instagram_media(coordinates, retsly_ids, 10)


def query_instagram_location():
	query_loc_id = 'https://api.instagram.com/v1/locations/search?lat=37.788900&lng=-122.3981040&client_id=f936a78d343c4f758fbb54a4ec51eb20'
	loc_obj = json.load(urllib2.urlopen(query_loc_id))
	pdb.set_trace()
	uid = 235311017
	query = 'https://api.instagram.com/v1/locations/' + str(uid) + '/media/recent?client_id=f936a78d343c4f758fbb54a4ec51eb20'
	media_obj = json.load(urllib2.urlopen(query))
	#query_instagram_location()


if __name__ == "__main__":
	sf_batch_full_pipeline()