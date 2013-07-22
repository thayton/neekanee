#!/usr/bin/env python

import os
import sys
import socket
import select

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.utils.encoding import smart_str, smart_unicode
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
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
        self.sock.sendto(smart_str(text), ('127.0.0.1', 31337))

        if isreadable(self.sock, self.timeout):
            data, addr = self.sock.recvfrom(2048)
            # print 'recv', data, 'from', addr

            #
            # This is tricky - the geocoding server may have created a new location
            # object and inserted it into the database. However, we will not see
            # that new object since our query set will be operating on our current
            # snapshot of the database. Because of this, we must force django to 
            # reload the data from the database:
            #
            # http://stackoverflow.com/questions/3346124/how-do-i-force-django-to-ignore-any-caches-and-reload-data
            #
            self.flush_transaction()

            pk = int(data)
            if pk >= 0:
                location = Location.objects.get(pk=pk)
                return location
            else:
                return None
        else:
            print 'neekanee_geocoder_client- timed out waiting for server'
            sys.exit(1)

    @transaction.commit_manually
    def flush_transaction(self):
        """
        Flush the current transaction so we don't read stale data
                
        Use in long running processes to make sure fresh data is read from
        the database.  This is a problem with MySQL and the default
        transaction mode.  You can fix it by setting
        "transaction-isolation = READ-COMMITTED" in my.cnf or by calling
        this function at the appropriate moment
        """
        transaction.commit()

if __name__ == '__main__':
    client = NeekaneeGeocoderClient()
    print client.geocode('rockville, md')
    print client.geocode('paris, france')
    print client.geocode('boston')
    print client.geocode('abcdefg')
    print client.geocode('Nassau, Bahamas')
