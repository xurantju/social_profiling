import numpy as np
import urllib
import urllib2
import json
import io, sys
import re, collections

finding_service_url = 'https://rets.io/api/v1/test_sf/listings?access_token=a9f17f30d3ff63cdd0bdba0cfb92e742&limit=100'

req = urllib2.Request(finding_service_url) # + urllib.urlencode(finding_service_params))
response = urllib2.urlopen(req)
response_json = json.loads(response.read())

#print response_json

item_list = response_json['bundle']
print len(item_list)
#print item_list
#item_list = response_data['item'] #response_json['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']

numdata = len(item_list)
#mapids = np.zeros((numdata, 1))
i = 0
data = []
for i in xrange(len(item_list)):
	#mapids[i] = item_list[i]['itemId'][0]
        #if 'id' not in item_list[i]:
        #    continue   
        #if 'address' not in item_list[i]:
        #    continue
        if 'coordinates' not in item_list[i]:
            print 'exception here'
            continue
        #if 'shortDescription' not in item_list[i]:
        #    print 'exception here'
        #    continue
        id = item_list[i]['id']
        address = item_list[i]['address']
        coordinates = item_list[i]['coordinates']
        data.append({'id':id, 'address':address, 'coordinates':coordinates})
        #shortDescription = item_list[i]['shortDescription'][0]
        i = i+1
        #print id, address, coordinates, #shortDescription

print json.dumps(data)
#with open('data.json', 'w') as f:
#    json.dumps(data,f) 

with io.open('data.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(data, ensure_ascii=False)))
