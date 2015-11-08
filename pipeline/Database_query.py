import json,httplib,urllib
import sys, pdb

class DatabaseQuery(object):

  def __init__(self, **kwargs):
    self.connection = httplib.HTTPSConnection('api.parse.com', 443)
    self.lg = kwargs['lg']
    self.la = kwargs['la']
    self.rg = kwargs['rg']

  def connect(self):
    if self.lg == None:
      print 'set lg'
      sys.exit(0)
    if self.la == None:
      print 'set la'
      sys.exit(0)
    if self.rg ==None:
      print 'set rg'
      sys.exit(0)

    self.params = urllib.urlencode({"where":json.dumps({
         "location": {
            "$nearSphere": {
              "__type": "GeoPoint",
              "latitude": self.la,
              "longitude": self.lg
            },
            "$maxDistanceInMiles": self.rg
          }
       })})   
    self.connection.connect()
    self.connection.request('GET', '/1/classes/Apartment?%s' % self.params, '', {
           "X-Parse-Application-Id": "lzjoICIugojwHnWEIBgTspWETcbE5noF1l68bWND",
           "X-Parse-REST-API-Key": "ZZONFDsBNQfyt5Jj5UPUNML1XrcjWcyjzTCOgnLK"
         })
    result = json.loads(self.connection.getresponse().read())
    return result

