#!/usr/bin/env python

"""
Import contents of ~/.NeekGeocoder into LocationAlias table
"""
import os
import sys
import string

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from neekanee_solr.models import *
from django.core.exceptions import ObjectDoesNotExist

def normalize_name(name):
    location = name.replace('&nbsp;', ' ')
    location = location.lower().strip()
    location = ','.join(['%s' % x.strip() for x in location.split(',')])
    location = '-'.join(['%s' % x.strip() for x in location.split('-')])
    return location

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <file>\n' % sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        try:
            d = eval(f.read())
            f.close()
        except IOError, e:
            sys.stderr.write('Open failed: %s\n' % e)
            sys.exit(1)

        for k,v in d['us'].items():
            state = k
            for l in v:
                city, (lat,lng), aliases = l

                try:
                    location = Location.objects.get(city=city, state=state, country='us')
                except ObjectDoesNotExist:
                    location = Location(city=city, state=state, country='us')
                    location.lat = lat
                    location.lng = lng
                    location.save()

                for alias in aliases:
                    alias = normalize_name(alias)
                    try:
                        location_alias = LocationAlias.objects.get(alias=alias)
                    except ObjectDoesNotExist:
                        location_alias = LocationAlias(location=location, alias=alias)
                        location_alias.save()
                                                       
