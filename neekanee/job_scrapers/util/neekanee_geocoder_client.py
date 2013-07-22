#!/usr/bin/env python

import os
import sys
import socket
import select

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *

def isreadable(sock, nsec):
    try:
        r,w,e = select.select([sock], [], [], nsec)
    except select.error, v:
        print 'Select generated an exception', v
        return 0
    else:
        return len(r)

class NeekaneeGeocoderClient():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = 5

    def geocode(self, text):
        self.sock.sendto(text, ('127.0.0.1', 31337))

        if isreadable(self.sock, self.timeout):
            data, addr = self.sock.recvfrom(2048)
            print 'recv', data, 'from', addr

            pk = int(data)
            if pk >= 0:
                location = Location.objects.get(pk=pk)
                print location, location.lat, location.lng
        else:
            print 'timed out waiting for server'
            sys.exit(1)

if __name__ == '__main__':
    client = NeekaneeGeocoderClient()
    client.geocode('rockville, md')
    client.geocode('paris, france')
    client.geocode('boston')


