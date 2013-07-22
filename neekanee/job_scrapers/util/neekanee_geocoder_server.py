#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

from neekanee_geocoder import NeekaneeGeocoder

class NeekaneeGeocoderServer(NeekaneeGeocoder):
    def __init__(self):
        NeekaneeGeocoder.__init__(self)
        self.return_usa_only = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 31337))

    def start(self):
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
    server.start()
