#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from script_instagram import _get_database, _get_pipeline
from pipeline import Pipeline, _load_obj, _save_json
from Database_query import DatabaseQuery
import pdb
PORT_NUMBER = 8000

global_pipeline = _get_pipeline('instagram')

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	'''
	def __init__(self, **kwargs):
		print 'start init pipeline'
		self.pipeline = _get_pipeline('instagram')
		print 'finish init pipeline'
	'''
	def parse_string(self):
		str_queries = dict()
		str_list = self.path.split("?")
		if len(str_list) < 2:
			return str_queries

		str_conds = str_list[1].split("&")
		for i in range(0,len(str_conds)):
			str_cond = str_conds[i].split("=")
			print(str_cond)
			str_queries[str_cond[0]] = str_cond[1]

		return str_queries

	#Handler for the GET requests
	def do_GET(self):
		print(self.path)
		queries = self.parse_string()
		if len(queries) > 0 :
			for k, v in enumerate(queries):
				print( v, queries[v])
				#pdb.set_trace()
			# do search database
			Database_query = _get_database(float(queries['longtitude']), float(queries['latitude']), 0.1)
			res = Database_query.connect()
			print len(res)
			for k2, v2 in enumerate(res):
				print k2, v2
				instagram_data = res[v2]
			print len(instagram_data)
			# assume only one house returned from database
			for k3, v3 in enumerate(instagram_data):
				data =  instagram_data[k3]
			# parse json
			address = data['address']
			latitude = data['location']['latitude']
			longitude = data['location']['longitude']
			inst_img_urls = data['inst_img_urls']
			inst_captions = data['inst_captions']
			name = data['name']
			print latitude, longitude, name, address

			# parse the string urls and captions to multiple instagram posts
			inst_urls = inst_img_urls.split('_!@#*()_')
			inst_captions = inst_captions.split('_!@#*()_')
			print len(inst_urls), len(inst_captions)
			print inst_urls[0], inst_captions[0]

			# do computation
			query_word = queries['class']
			return_urls, return_text = global_pipeline.post_retrieval_without_uid(inst_urls, inst_captions, query_word)
				
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# Send the html message
			for i in xrange(len(return_urls)):
				self.wfile.write(return_urls[i] +',')
				#self.wfile.write("https://s3.amazonaws.com/retsly_images_production/test_sf/P_55ceef56a452956edae07555/2.jpg")

		return

	


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	#server.start_pipeline()
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()