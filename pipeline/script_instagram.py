import pdb
import json, urllib2

from pipeline import Pipeline, _load_obj, _save_json

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

def more_sf_data(save_name):
	coordinates, address, retsly_ids = pipeline.query_retsly_v1()
	try:
		sf_data = _load_obj(save_name)
	except:
		pipeline.query_instagram_media(coordinates, retsly_ids, save_name, 10)


def write_json_sf_top5():
	obj_name = 'static_10_sf_city_larger'
	sf_data = _load_obj(obj_name)
	coordinates, address, retsly_ids, house_img_urls, descriptions = pipeline.query_retsly_v1()
	# totall 11
	# select top 5 locations
	post_nums = []
	instagram_top_5_house = dict()
	for k,v in enumerate(sf_data):
		print k,v # v is id for one listing
		idx = retsly_ids.index(v)
		print retsly_ids[idx], address[idx], house_img_urls[idx], descriptions[idx]
		#urls, text = pipeline.post_retrieval(sf_data[v], query)
		instgram_data = sf_data[v]
		post_nums.append(len(instgram_data))
		if len(instgram_data) >= 196:
			instagram_top_5_house[v] = instgram_data

	sf_test_top_5_house = []
	for k, v in enumerate(instagram_top_5_house):
		print k, v
		idx = retsly_ids.index(v)
		sf_test_top_5_house.append({'name' : retsly_ids[idx], 'latitude' : float(coordinates[idx][1]),
			'longitude' : float(coordinates[idx][0]), 'url' : house_img_urls[idx], 'description' : descriptions[idx],
			'address' : address[idx]})
		# store house info to json
		pdb.set_trace()

	with open('sf_test_top_5_house.json', 'w') as fp:
		json.dump(sf_test_top_5_house, fp)

	pdb.set_trace()	
'''
"name": config[i]['name'],
"des": config[i]['des'],
"location": {
"__type": "GeoPoint",
"latitude": config[i]['latitude'],
"longitude": config[i]['longitude']
},
"date": {
"__type": "Date",
"iso": config[i]['date']
},
"url": config[i]['url']
}), {
'''
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
	#urls, text = single_address_full_pipeline(pipeline, query)
	#more_sf_data('static_10_sf_city_larger')
	write_json_sf_top5()
	pdb.set_trace()