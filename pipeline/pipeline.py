"""
backend pipeline
"""

# general
import numpy as np 
import pdb

# step 1: instgram and zillow API
import urllib2
import json

# step 2: text summarization

class Pipeline(object):

	def __init__(self, **kwargs):
		self.data_source = 'instgram'

	@staticmethod
	def query_instagram_location(location_id, max_queries):
		query_loc_id = 'https://api.instagram.com/v1/locations/search?lat=48.858844&lng=2.294351&client_id=f936a78d343c4f758fbb54a4ec51eb20'
		loc_obj = json.load(urllib2.urlopen(query_loc_id))
		pdb.set_trace()
		#query = 'https://api.instagram.com/v1/locations/{location-id}/media/recent?access_token=f936a78d343c4f758fbb54a4ec51eb20'
		#retrieved = []
		#for pages in xrange(max_queries):
