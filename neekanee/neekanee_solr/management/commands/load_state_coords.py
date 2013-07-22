#!/usr/bin/env python

import os
import sys
import time

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *

"""
Used to import lat,lng coordinates for each of the 50 states
into Location table in database.
"""
from geopy import geocoders

STATES = {
    'AL': "Alabama",
    'AK': "Alaska",
    'AZ': "Arizona",
    'AR': "Arkansas",
    'CA': "California",
    'CO': "Colorado",
    'CT': "Connecticut",
    'DE': "Delaware",
    'DC': "District of Columbia",
    'FL': "Florida",
    'GA': "Georgia",
    'HI': "Hawaii",
    'ID': "Idaho",
    'IL': "Illinois",
    'IN': "Indiana",
    'IA': "Iowa",
    'KS': "Kansas",
    'KY': "Kentucky",
    'LA': "Louisiana",
    'ME': "Maine",
    'MD': "Maryland",
    'MA': "Massachusetts",
    'MI': "Michigan",
    'MN': "Minnesota",
    'MS': "Mississippi",
    'MO': "Missouri",
    'MT': "Montana",
    'NE': "Nebraska",
    'NV': "Nevada",
    'NH': "New Hampshire",
    'NJ': "New Jersey",
    'NM': "New Mexico",
    'NY': "New York",
    'NC': "North Carolina",
    'ND': "North Dakota",
    'OH': "Ohio",
    'OK': "Oklahoma",
    'OR': "Oregon",
    'PA': "Pennsylvania",
    'RI': "Rhode Island",
    'SC': "South Carolina",
    'SD': "South Dakota",
    'TN': "Tennessee",
    'TX': "Texas",
    'UT': "Utah",
    'VT': "Vermont",
    'VA': "Virginia",
    'WA': "Washington",
    'WV': "West Virginia",
    'WI': "Wisconsin",
    'WY': "Wyoming"
}

STATE_COORDS = {
    'wa': (47.751074099999997, -120.74013859999999),
    'de': (38.910832499999998, -75.527669900000006), 
    'dc': (38.895111800000002, -77.036365799999999), 
    'wi': (43.7844397, -88.787867800000001), 
    'wv': (38.597626200000001, -80.454902599999997), 
    'hi': (19.896766199999998, -155.58278179999999), 
    'fl': (27.6648274, -81.515753500000002), 
    'wy': (43.075967800000001, -107.29028390000001), 
    'nh': (43.193851600000002, -71.572395299999997), 
    'nj': (40.058323799999997, -74.405661199999997), 
    'nm': (34.972730499999997, -105.0323635), 
    'tx': (31.968598799999999, -99.901813099999998), 
    'la': (31.244823400000001, -92.145024500000005), 
    'ak': (63.588752999999997, -154.49306189999999), 
    'nc': (35.759573099999997, -79.019299700000005), 
    'nd': (47.551492600000003, -101.0020119), 
    'ne': (41.492537400000003, -99.901813099999998), 
    'tn': (35.517491300000003, -86.580447300000003), 
    'ny': (40.7143528, -74.005973100000006), 
    'pa': (41.203321600000002, -77.194524700000002), 
    'ri': (41.580094500000001, -71.477429099999995), 
    'nv': (38.802609699999998, -116.419389), 
    'va': (37.431573399999998, -78.656894199999996), 
    'co': (39.5500507, -105.7820674), 
    'ca': (36.778261000000001, -119.4179324), 
    'al': (32.318231400000002, -86.902298000000002), 
    'ar': (35.201050000000002, -91.831833399999994), 
    'vt': (44.558802800000002, -72.577841500000005), 
    'il': (40.633124899999999, -89.398528299999995), 
    'ga': (32.157435100000001, -82.907122999999999), 
    'in': (40.551216500000002, -85.602364300000005), 
    'ia': (41.878002500000001, -93.097701999999998), 
    'ma': (42.4072107, -71.382437400000001), 
    'az': (34.048928099999998, -111.0937311), 
    'id': (44.068201899999998, -114.7420408), 
    'ct': (41.603220700000001, -73.087749000000002), 
    'me': (45.253782999999999, -69.445468899999995), 
    'md': (39.045754899999999, -76.641271200000006), 
    'ok': (35.007751900000002, -97.092877000000001), 
    'oh': (40.417287100000003, -82.907122999999999), 
    'ut': (39.3209801, -111.0937311), 
    'mo': (37.964252899999998, -91.831833399999994), 
    'mn': (46.729553000000003, -94.685899800000001), 
    'mi': (44.314844299999997, -85.602364300000005), 
    'ks': (39.011901999999999, -98.484246499999998), 
    'mt': (46.879682199999998, -110.3625658), 
    'ms': (32.354667900000003, -89.398528299999995), 
    'sc': (33.836081, -81.163724500000001), 
    'ky': (37.839333199999999, -84.270017899999999), 
    'or': (43.804133399999998, -120.55420119999999), 
    'sd': (43.969514799999999, -99.901813099999998)
}


if __name__ == '__main__':
    for state,(lat,lng) in STATE_COORDS.items():
        try:
            l = Location.objects.get(city='', state=state, country='us')
        except ObjectDoesNotExist:
            l = Location(city='', state=state, country='us', lat=lat, lng=lng)
            l.save()
        else:
            print 'Warning - location already exists: %s' % l
