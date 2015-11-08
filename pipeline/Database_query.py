import json,httplib,urllib
import sys

if __name__ == '__main__':
      connection = httplib.HTTPSConnection('api.parse.com', 443)
      lg = float(sys.argv[1])
      la = float(sys.argv[2])
      rg = float(sys.argv[3])
      params = urllib.urlencode({"where":json.dumps({
             "location": {
                "$nearSphere": {
                  "__type": "GeoPoint",
                  "latitude": lg,
                  "longitude": la
                },
                "$maxDistanceInMiles": rg
              }
           })})

      connection.connect()
      connection.request('GET', '/1/classes/Apartment?%s' % params, '', {
             "X-Parse-Application-Id": "lzjoICIugojwHnWEIBgTspWETcbE5noF1l68bWND",
             "X-Parse-REST-API-Key": "ZZONFDsBNQfyt5Jj5UPUNML1XrcjWcyjzTCOgnLK"
           })
      result = json.loads(connection.getresponse().read())
      print result