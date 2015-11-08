"""
backend pipeline
"""

# general
import os, sys
import numpy as np 
import pdb

# step 1: instgram and zillow API
import urllib2
import json
import pickle

# step 2: text summarization
from gensim.models import Word2Vec
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
import re
import operator
from itertools import izip
import requests
from PIL import Image
from StringIO import StringIO

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
		self.retrieve_top = 9
		self.locations = None
		self.image_dir = '/home/parallels/ranxu/data/images/'
		self.city = 'sf'
		dirname = os.path.dirname(self.image_dir + self.city)
		try:
		    os.stat(dirname)
		except:
		    os.mkdir(dirname)   
		# before 11.6.23.59.59; 11.5.23.59.59; 11.4.23.59.59; 11.3.23.59.59; 11.2.23.59.59
		self.epoch_timestamps = ['1446951599', '1446883199', '1446796799', '1446710399', '1446623999',
			'1446537599', '1446451199', '1446361199', '1446274799', '1446188399', '1446101999', '1446015599',
			'1445929199', '1445842799', '1445756399', '1446857999', '1446771599', '1446685199', '1446598799',
			'1446512399', '1446425999', '1446335999', '1446249599', '1446163199', '1446076799']
		print 'loading wordvec model: 3.6GB'
		#self.wordvec_model = Word2Vec.load_word2vec_format('/home/parallels/ranxu/data/GoogleNews-vectors-negative300.bin', binary=True)

	@staticmethod
	def query_instagram_location(geolocation_tuple):
		lat = str(geolocation_tuple[1])
		lng = str(geolocation_tuple[0])
		query_loc_id = 'https://api.instagram.com/v1/locations/search?lat=' + lat + '&lng=' + lng + '&client_id=f936a78d343c4f758fbb54a4ec51eb20'
		query = 'https://api.instagram.com/v1/media/search?lat=' + lat + '&lng=' + lng + '&client_id=f936a78d343c4f758fbb54a4ec51eb20'
		loc_obj = json.load(urllib2.urlopen(query_loc_id))
		#retrieved = []
		#for pages in xrange(max_queries):

	# step 1: retsly API
	@staticmethod
	def query_retsly_v1():
		# first, test data.json from test_sf 
		coordinates = []
		address = []
		retsly_ids = []
		house_image_urls = []
		descriptions = []
		data = _load_json('data/data_sf.json')
		for line in data:
			coordinates.append(line['coordinates'])
			address.append(line['address'])
			retsly_ids.append(line['id'])
			house_image_urls.append(line['url'])
			descriptions.append(line['shortDescription'])
		return coordinates, address, retsly_ids, house_image_urls, descriptions

	# step 2: retrieve instagram media from retsly geolocation
	def query_instagram_media(self, geolocation_tuples, retsly_ids, save_name, max_queries=5):
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
		_save_obj(retsly_data, save_name)

	# step 3: do tag/key word retrieval
	def post_retrieval(self, retsly_data, query):

		def tokenizer(text, stop_words):
			words = re.sub("[^a-zA-Z]", " ", text).split()
			filtered_words = [w for w in words if not w in stop_words]
			return filtered_words

		def get_wordvec_similarity(words):
			return_sims = []
			for word in words:
				try:
					sim = self.wordvec_model.similarity(word, query)
					return_sims.append(sim)
				except KeyError:
					# instagram word is not in wordvec dicitonary
					pass
			return return_sims

		# store wordvec similarities over all instagram posts
		inst_similarities = dict()
		for k,v in enumerate(retsly_data):
			#print k, v # v is instagram uid
			instance = retsly_data[v]
			if instance['caption'] == None:
				continue
			caption_text = instance['caption']['text']
			# clean text
			filtered_captions = tokenizer(caption_text, stop_words)
			# do similarity over captions
			caption_sims = get_wordvec_similarity(filtered_captions) # check None
			# do similarity over commets 
			#comments_sims = []
			# do not process comments
			'''
			if instance['comments'] != None:
				filtered_comments = []
				for i in xrange(len(instance['comments'])):
					comment_text = instance['comments'][i]['text']
					filtered_comments += tokenizer(caption_text, stop_words)
				comments_sims = get_wordvec_similarity(filtered_comments)
			'''
			try:
				#mean_sim = (np.sum(caption_sims) + np.sum(comments_sims)) / float(len(comments_sims) + len(caption_sims))
				#mean_sim = np.sum(caption_sims) / float(len(caption_sims))
				# maybe only select top 3-5 word
				topN = np.min((3, len(caption_sims)))
				top_sim = np.sort(caption_sims)[-topN:]
				mean_sim = np.sum(top_sim) / float(topN)

				#print np.sum(caption_sims) + np.sum(comments_sims), float(len(comments_sims) + len(caption_sims)), mean_sim
			except:
				# no words, though we already checked caption...anyway...
				mean_sim = -1
			if not np.isnan(mean_sim):
				inst_similarities[v] = mean_sim
		sorted_sim = sorted(inst_similarities.items(), key=operator.itemgetter(1), reverse=True)

		# retrieve top 9
		max_retrieved = np.min((len(sorted_sim), self.retrieve_top))
		top_selection = sorted_sim[:max_retrieved]
		return_urls = []
		return_text = []
		for i in xrange(len(top_selection)):
			score = top_selection[i][1]
			#pdb.set_trace()
			inst_id = top_selection[i][0]
			inst_data = retsly_data[inst_id]
			text = None
			if inst_data['caption'] != None:
				text = inst_data['caption']['text']
				print text
			if inst_data['img'] != None:
				rr = requests.get(inst_data['img'], allow_redirects=False, timeout=10.00)
				if rr.status_code == 200:
					# download the image
					if Image.open(StringIO(rr.content)).getbbox() != None:
						fpath = os.path.join(self.image_dir, self.city, inst_id+'_'+query+'_top_'+str(i))
						Image.open(StringIO(rr.content)).save(fpath, 'JPEG', quality=100)
					return_urls.append(inst_data['img'])
					return_text.append(text)
				#pdb.set_trace()
		return return_urls, return_text