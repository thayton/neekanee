#!/usr/bin/env python

import os
import re
import sys
import pwd
import json
import time
import pprint

from geopy import geocoders

def geocode(location):
    homedir = pwd.getpwnam(os.getlogin()).pw_dir
    cache_file = os.path.join(homedir, '.NeekGeocoder')

    g = NeekGeocoder()
    g.load_cache_from_file(cache_file)
    r = g.geocode(location)
    g.save_cache_to_file(cache_file)

    return r

#
# The cache is keyed in a hierarchy by country and then state. Underneath
# each state is a list of cities in that state along with a list of names
# used to identify the location.
#
# cache = {
#   'us': {
#     'md': [ 
#       ('bethesda',  (38.9,-77.1), [ "md-bethesda" ]),
#       ('rockville', (39.8,-77.1), [ "rockville,md", "rockville, usa", "md-rockville" ]) 
#     ]
#     ...
#   }
# }
#
class NeekGeocoder():
    def __init__(self):
        self.cache = { 'us': {} }
        self.geocoder = geocoders.Google()
        self.debug = False

    def geocode(self, location):
        # XXX duplicate/similar code as in normalize name - refactor
        location = self.strip_entity_refs(location)
        location = location.lower().strip()
        location = ','.join(['%s' % x.strip() for x in location.split(',')])
        location = '-'.join(['%s' % x.strip() for x in location.split('-')])

        entry = self.get_cache_entry(location)
        if entry is None:
            try:
                if self.debug:
                    sys.stderr.write('** Cache miss for "%s"\n' % location)
            except:
                pass

            ntries = 0
            while ntries < 2:
                try:
                    results = self.geocoder.geocode(location, exactly_one=False)
                except geocoders.google.GTooManyQueriesError:
                    sys.stderr.write('Slowing down geocoder requests...\n')
                    time.sleep(1)
                    ntries += 1
                    continue
                except Exception,e:
                    try:
                        sys.stderr.write('Can\'t geocode %s - %s\n' % (location, e))
                    except:
                        pass

                    return None

                break

            if len(results) > 1:
                sys.stderr.write('Warning: more than one result returned for %s\n' % location)

            normal_name = None
            for result in results:
                place, coord = result
                if place is not None:
                    normal_name = self.normalize_name(place)
                    if normal_name:
                        break

            if normal_name is None:
                return None

            self.add_cache_entry(normal_name, coord, location)

            #
            # normal_name: { 'city': 'rockville', 'state': 'md', 'country': 'us' }
            #
            entry = normal_name
            entry['coord'] = coord
        else:
            if self.debug:
                sys.stderr.write('** Cache hit for "%s"\n' % location)

        return entry

    def normalize_name(self, place):
        """
        Normalize the place name into a JSON representaion. The place
        variable is generally the address that Google sends back to us
        when we geocode a location. For example, if we ask Google to
        geocode 'md-rockville', we will get back the string

          '335 Charles St, Rockville, MD 20850, USA' 

        This function will normalize that string into the follow JSON 
        represenation:
        
          {'city': 'rockville', 'state': 'md', 'country': 'us'}
           
        """
        place = self.strip_entity_refs(place)
        place = ['%s' % x.strip() for x in place.split(',')]
        country = place[-1]
    
        if country != 'USA':
            # Only do US locations for now
            return None

        if len(place) < 3:
            # Missing city
            return None

        # extract the state and remove any zip codes
        state = place[-2][:2].lower().strip()
        state = state[:2]
        city = place[-3].lower()

        normalized_name = {'city': city, 'state': state, 'country': 'us'}
        return normalized_name
        
    def strip_entity_refs(self, string):
        string = string.replace('&nbsp;', ' ')
        # others? ...
        return string

    def get_cache_entry(self, location):
        """
        Given a name like 'NYC, NY' return::
        
        {'city': new york, 'state': 'ny', 'country': 'us', 'coord': (41.2,23.4)}
        """
        location = location.lower()

        for state,cities in self.cache['us'].items():
            for city in cities:
                city_name, coord, aliases = city
                if city_name == location:
                    return {'city': city_name, 'state': state, 'country': 'us', 'coord': coord}
                else:
                    for alias in aliases:
                        if location == alias:
                            return {'city': city_name, 'state': state, 'country': 'us', 'coord': coord}

        return None

    def add_cache_entry(self, normalized_name, coord, location):
        #
        # Only count a string as an alias of the city if it's 
        # actually different from the city name
        #
        location = location.lower()
        if normalized_name['city'] != location:
            alias = [location]
        else:
            alias = []

        state = normalized_name['state']
        if not self.cache['us'].has_key(state):
            entry = {}
            entry = (normalized_name['city'], coord, alias)
            self.cache['us'][state] = [entry]
        else:
            entry_added = False
            for city in self.cache['us'][state]:
                city_name, aliases = city[0],city[2]
                if city_name == normalized_name['city']:
                    aliases.extend(alias)
                    entry_added = True
                    break

            if entry_added == False:
                entry = (normalized_name['city'], coord, alias)
                self.cache['us'][state].append(entry)

    def save_cache_to_file(self, file):
        try:
            with open(file, 'w') as f:
                pp = pprint.PrettyPrinter(indent=2, stream=f)
                pp.pprint(self.cache)
                f.close()
        except IOError:
            pass

    def load_cache_from_file(self, file):
        try:
            with open(file, 'r') as f:
                self.cache = eval(f.read())
                f.close()
        except IOError:
            pass

if __name__ == '__main__':
    g = NeekGeocoder()
    print g.geocode('rockville')
    print g.geocode('rockville')
    print g.geocode('bethesda')
    print g.geocode('bethesda')
    print g.geocode('bethesda, md')
    print g.geocode('vienna, austria')
    print g.geocode('US- DC')
    print g.geocode('cambridge or new york us000')
    print g.geocode('richmond&nbsp;,virginia&nbsp;')
    g.save_cache_to_file('.NeekGeocoder')
    
