"""
backend pipeline
"""

# general
import numpy as np 
import pdb

# step 1: instgram and zillow API
import urllib2
import json
import pickle

# step 2: text summarization

# utils
def _save_obj(obj, name):
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def _load_obj(name):
	f = open(name + '.pkl', 'rb')
	return pickle.load(f)

def _save_json(data, name):
	obj = open(name, 'wb')
	obj.write(data)
	obj.close

def _load_json(name):
	with open(name) as data_file:    
		data = json.load(data_file)
	return data

# whole pipeline class
class Pipeline(object):

	def __init__(self, **kwargs):
		self.data_source = 'instgram'
		self.instgram_radius = 500
		self.min_posts_per_listing = 100
		self.locations = None
		# before 11.6.23.59.59; 11.5.23.59.59; 11.4.23.59.59; 11.3.23.59.59; 11.2.23.59.59
		self.epoch_timestamps = ['1446883199', '1446796799', '1446710399', '1446623999',
			'1446537599', '1446451199', '1446361199', '1446274799', '1446188399', '1446101999']

	@staticmethod
	def query_instagram_location(geolocation_tuple):
		lat = str(geolocation_tuple[1])
		lng = str(geolocation_tuple[0])
		query_loc_id = 'https://api.instagram.com/v1/locations/search?lat=' + lat + '&lng=' + lng + '&client_id=f936a78d343c4f758fbb54a4ec51eb20'
		query = 'https://api.instagram.com/v1/media/search?lat=' + lat + '&lng=' + lng + '&client_id=f936a78d343c4f758fbb54a4ec51eb20'
		loc_obj = json.load(urllib2.urlopen(query_loc_id))
		#retrieved = []
		#for pages in xrange(max_queries):

	@staticmethod
	def query_retsly_v1():
		# first, test data.json from test_sf 
		coordinates = []
		address = []
		retsly_ids = []
		data = _load_json('data/data.json')
		for line in data:
			coordinates.append(line['coordinates'])
			address.append(line['address'])
			retsly_ids.append(line['id'])
		return coordinates, address, retsly_ids

	def query_instagram_media(self, geolocation_tuples, retsly_ids, max_queries=5):
		# assume input a batch of geolocation
		retsly_data = dict()
		for num_query in xrange(len(geolocation_tuples)):
			if num_query > max_queries:
				break
			geolocation_tuple = geolocation_tuples[num_query]
			retsly_id = retsly_ids[num_query]
			# for each listed house
			lat = str(geolocation_tuple[1])
			lng = str(geolocation_tuple[0])
			instagram_data = dict()
			# query min_posts_per_listing
			print 'queryng ... lat/lng %s %s' % (lat, lng)
			radius = str(self.instgram_radius)
			query_time = 0
			for i in xrange(len(self.epoch_timestamps)):
				timestamp = self.epoch_timestamps[i]
				print timestamp
				query = 'https://api.instagram.com/v1/media/search?lat=' + lat \
					+ '&lng=' + lng + '&client_id=f936a78d343c4f758fbb54a4ec51eb20&distance=' \
					+ str(radius) + '&max_timestamp=' + timestamp
				media_obj = json.load(urllib2.urlopen(query))
				query_time += 1
				for line in media_obj['data']:
					img = line['images']['standard_resolution']['url']
					caption = line['caption'] # find caption['text'] is it's not None
					#caption = line['caption']['text']
					comments = line['comments']['data'] # maybe a number of comments
					ids = line['id']
					created_time = line['created_time']
					if not ids in instagram_data:
						data = {'img' : img, 'caption' : caption, 'comments' : comments, 'ids' : ids, 'created_time' : created_time}
						instagram_data[ids] = data
				print 'query %d times stored instance %d ' % (query_time, len(instagram_data))		
			retsly_data[retsly_id] = instagram_data
		_save_obj(retsly_data, 'static_10_sf_city')