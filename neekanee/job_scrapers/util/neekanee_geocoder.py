#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time

from geopy import geocoders
from isocodes import country_name_to_code, state_name_to_code

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *

class NeekaneeGeocoder():
    def __init__(self):
        self.geocoder = geocoders.Google()
        self.debug = False
        self.return_usa_only = False # Only return locations within USA

    def geocode(self, text):
        """
        Determine lat,lng pair for location text. Lookup (or create) Location
        object associated with text and return to caller.
        """
        text = self.normalize_string(text)

        try:
            null_location = NullLocation.objects.get(text=text)
        except ObjectDoesNotExist:
            pass
        else:
            # It's in NullLocation because it can't be geocoded
            return None

        try:
            location_alias = LocationAlias.objects.get(alias=text)
        except ObjectDoesNotExist:
            pass
        else:
            if len(location_alias.location.city) > 0:
                if self.return_usa_only:
                    if location_alias.location.country == 'us':
                        return location_alias.location
                    else:
                        return None
                else:
                    return location_alias.location
            else:
                return None

        location_alias = LocationAlias(alias=text)

        place,coord = self._geocode(text)

        if place is None:
            null_location = NullLocation(text=text)
            try:
                null_location.save()
            except:
                pass
            return None

        defaults = { 'lat': coord[0], 'lng': coord[1] }
        place.update({'defaults': defaults})

        location_alias.location,_ = Location.objects.get_or_create(**place)
        location_alias.save()

        #
        # Since only the job scrapers should be using this code, only return
        # locations with the city set. Otherwise, the location drill-down in
        # the front-end won't work correctly
        #
        if len(place['city']) > 0:
            if self.return_usa_only:
                if place['country'] == 'us':
                    return location_alias.location
                else:
                    return None
            else:
                return location_alias.location
        else:
            return None

    def _geocode(self, location):
        """
        Return dictionary with city,state,country keys set to values
        from location and a lat,lng tuple for that location.
        """
        results = []
        ntries = 0

        while ntries < 2:
            try:
                time.sleep(0.5)
                results = self.geocoder.geocode(location, exactly_one=False)
            except geocoders.google.GTooManyQueriesError:
                time.sleep(1)
                ntries += 1
                continue
            except Exception,e:
                try:
                    sys.stderr.write('Can\'t geocode %s - %s\n' % (location, e))
                except:
                    pass

            break

        for place, coord in results:
            if place is not None:
                result = self.extract_fields(place)
                if result:
                    return result, coord

        return None, None

    def extract_fields(self, place):
        """
        Given location string extract city, state, country. Return
        dictionary result with those fields as keys.
        """
        place = self.strip_entity_refs(place)
        place = ['%s' % x.strip().lower() for x in place.split(',')]

        country = place[-1]

        if len(country) == 2:
            country_code = country
        else:
            if country_name_to_code.has_key(country):
                country_code = country_name_to_code[country]
            else:
                sys.stderr.write('No country code for %s\n' % country)
                return None

        if country_code == 'us':
            if len(place) < 3:
                # Missing city
                return None

            # extract the state and remove any zip codes
            state = place[-2].split()[0]

            if len(state) > 2:
                state = state_name_to_code[state]
            else:
                state = state[:2]

            city = place[-3]

            result = {'city': city, 'state': state, 'country': country_code}
        elif country_code in [ 'ca', 'in' ]:
            if len(place) >= 3:
                city = place[-3]
            else:
                city = ''

            result = {'city': city, 'country': country_code}
        else:
            if len(place) < 2:
                result = {'city': '', 'country': country_code }
            else:
                result = {'city': place[-2], 'country': country_code}

        return result

    def strip_entity_refs(self, string):
        string = string.replace('&nbsp;', ' ')
        # others? ...
        return string

    def normalize_string(self, string):
        string = self.strip_entity_refs(string)
        string = string.lower().strip()
        string = ','.join(['%s' % x.strip() for x in string.split(',')])
        string = '-'.join(['%s' % x.strip() for x in string.split('-')])
        return string

if __name__ == '__main__':
    g = NeekaneeGeocoder()
    print g.geocode('jeddah saudi arabia')
    print g.geocode('ottawa, canada')
    print g.geocode('paris, france')
    print g.geocode('beijing')
    print g.geocode('rockville-md-usa')
    print g.geocode('usa-md-rockville')
    print g.geocode('canada-thornhill,toronto')
    print g.geocode('New Delhi, India')
    print g.geocode('Mumbai, India')

    print g.geocode('other')

    g.return_usa_only = False
    print g.geocode('linköping,sweden')
    print g.geocode('singapore, singapore')
    print g.geocode('false river, lousiana')
