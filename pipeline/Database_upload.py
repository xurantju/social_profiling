import json,httplib
import sys

if __name__ == '__main__':
    config = json.loads(open(sys.argv[1]).read())
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    
    for i in range(len(config)):
      print(i)  
      #imgpath = config[i]['image']
       # remotepath = '/1/files/zillow%06d.jpg' % i
       # connection.request('POST', remotepath, open(imgpath, 'rb').read(), {
       #     "X-Parse-Application-Id": "lzjoICIugojwHnWEIBgTspWETcbE5noF1l68bWND",
       #     "X-Parse-REST-API-Key": "ZZONFDsBNQfyt5Jj5UPUNML1XrcjWcyjzTCOgnLK",
       #     "Content-Type": "image/jpeg"
       #     })
       # result = json.loads(connection.getresponse().read())
       # print result['name']

        connection.request('POST', '/1/classes/Apartment', json.dumps({
                                                              "name": config[i]['name'],
                                                              "description": config[i]['description'],
                                                              "location": {
                                                              "__type": "GeoPoint",
                                                              "latitude": config[i]['latitude'],
                                                              "longitude": config[i]['longitude']
                                                              },
                                                              "inst_img_urls" : config[i]['inst_img_urls'],
                                                              "inst_captions" : config[i]['inst_captions'],
                                                              "address": config[i]['address'], 
                                                              "url": config[i]['url']
                                                              }), {
                   "X-Parse-Application-Id": "lzjoICIugojwHnWEIBgTspWETcbE5noF1l68bWND",
                   "X-Parse-REST-API-Key": "ZZONFDsBNQfyt5Jj5UPUNML1XrcjWcyjzTCOgnLK",
                   "Content-Type": "application/json"
                   })
        results = json.loads(connection.getresponse().read())
        print results
