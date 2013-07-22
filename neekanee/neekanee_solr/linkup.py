# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

API_PATH = 'http://www.linkup.com/developers/v-1/search-handler.js'
API_KEY = '27BA49683B3AB77DB612969C8484270A'
SEARCH_KEY = '76d8f726d05ebf20fa1e7942cf98f389'

class LinkUpResults(object):
    def __init__(self, response):
        try:
            self.response = json.loads(response)
            self.sponsored_listings = self.response.get('sponsored_listings', [])
        except:
            self.response = None
            self.sponsored_listings = None

class LinkUp(object):
    def __init__(self):
        self.headers = {'User-agent': 'Neekanee'}
        self.params = {
            'api_key': API_KEY,
            'embedded_search_key': SEARCH_KEY,
            'include_organic': '0',
            'desc_length': '210'
        }

    def search(self, remote_addr, keyword=None, location=None, company=None):
        params = {}
        params['orig_ip'] = remote_addr
        params.update(self.params)

        if keyword:
            params['keyword'] = keyword
            
        if location:
            params['location'] = location

        if company:
            params['company'] = company

        data = urllib.urlencode(params) 
        request = urllib2.Request(API_PATH, data=data, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()
    
if __name__ == '__main__':
    linkup = LinkUp()

    response = linkup.search('software engineer', 'Rockville, MD')
    sponsored_listings = LinkUpResults(response).sponsored_listings
    print json.dumps(sponsored_listings, indent=4)

    response = linkup.search(keyword='java developer')
    sponsored_listings = LinkUpResults(response).sponsored_listings
    print json.dumps(sponsored_listings, indent=4)

    response = linkup.search(location='Rockville, MD')
    sponsored_listings = LinkUpResults(response).sponsored_listings
    print json.dumps(sponsored_listings, indent=4)

    response = linkup.search()
    sponsored_listings = LinkUpResults(response).sponsored_listings
    print json.dumps(sponsored_listings, indent=4)
