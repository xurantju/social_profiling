import pdb
import json, urllib2

from pipeline import Pipeline, _load_obj

def _get_pipeline(data_source):
	return Pipeline(data_source=data_source)


def single_address_full_pipeline(pipeline, query):
	# step 1: query retsly to get listing geolocation
	coordinates, address, retsly_ids = pipeline.query_retsly_v1()
	sf_data = _load_obj('static_10_sf_city')
	max_listing = 3
	ids = 0
	for k,v in enumerate(sf_data):
		print k,v # v is id for one listing
		idx = retsly_ids.index(v)
		print retsly_ids[idx], address[idx]
		urls, text = pipeline.post_retrieval(sf_data[v], query)
		ids += 1
		if ids >= max_listing:
			break
	return urls, text

def sf_batch_full_pipeline(pipeline, query):

	# step 1: query retsly to get listing geolocation
	coordinates, address, retsly_ids = pipeline.query_retsly_v1()
	# get instgram media data
	#geolocation_tuple = [-122.4120249,37.73691843]
	#current_loc_trulia = [-122.3981040, 37.788900]

	# step 2: query instagram to get social media data
	try:
		sf_data = _load_obj('static_10_sf_city')
	except:
		pipeline.query_instagram_media(coordinates, retsly_ids, 10)

	# step 3: build wordvec similarities and topics from each listing 
	for k,v in enumerate(sf_data):
		print k,v # v is id for one listing
		idx = retsly_ids.index(v)
		print retsly_ids[idx], address[idx]
		urls, text = pipeline.post_retrieval(sf_data[v], query)
		pdb.set_trace()


def query_instagram_location():
	query_loc_id = 'https://api.instagram.com/v1/locations/search?lat=37.788900&lng=-122.3981040&client_id=f936a78d343c4f758fbb54a4ec51eb20'
	loc_obj = json.load(urllib2.urlopen(query_loc_id))
	pdb.set_trace()
	uid = 235311017
	query = 'https://api.instagram.com/v1/locations/' + str(uid) + '/media/recent?client_id=f936a78d343c4f758fbb54a4ec51eb20'
	media_obj = json.load(urllib2.urlopen(query))
	#query_instagram_location()


if __name__ == "__main__":
	query = 'restaurant'
	pipeline = _get_pipeline('instagram')
	#sf_batch_full_pipeline(query)
	urls, text = single_address_full_pipeline(pipeline, query)
	pdb.set_trace()