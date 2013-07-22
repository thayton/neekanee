#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

from neekanee.daemon import Daemon
from neekanee.geocoder.neekanee_geocoder import NeekaneeGeocoder

class NeekaneeGeocoderServer(NeekaneeGeocoder, Daemon):
    """
    Geocoder running as a server so that multiple plugins can do geocoding at the
    same time. We serialize plugin geocoding requests through this server to prevent
    multiple plugins hitting the Google geocoding service at the same time and to 
    prevent database race conditions.

    The server tries to geocode text it receives from a client, and if it's successful
    it sends back the primary key of the location corresponding to the text.
    """
    def __init__(self, pidfile='/var/run/neekanee/neekanee_geocoder.pid'):
        NeekaneeGeocoder.__init__(self)
        Daemon.__init__(self, pidfile=pidfile)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 31337))

        while True:
            data, addr = self.sock.recvfrom(2048)
            print 'recv', data, 'from', addr

            location = self.geocode(data)
            
            if location is not None:
                self.sock.sendto('%d' % location.pk, addr)
            else:
                self.sock.sendto('-1', addr)

if __name__ == '__main__':
    server = NeekaneeGeocoderServer()

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            server.start()
        elif 'stop' == sys.argv[1]:
            server.stop()
        elif 'restart' == sys.argv[1]:
            server.restart()
        else:
            print "Unknown command"
            sys.exit(2)
            sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
