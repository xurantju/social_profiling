#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
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
		for k, v in enumerate(queries):
			print( v, queries[v])
			
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("https://s3.amazonaws.com/retsly_images_production/test_sf/P_55ceef56a452956edae07555/1.jpg")
		return

	


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()