#!/usr/bin/env python

import os
import sys
import httplib
import urlparse
import mechanize

if len(sys.argv) != 2:
    sys.stderr.write('usage: %s <url>\n' % sys.argv[0])
    sys.exit(1)

url = sys.argv[1]
o = urlparse.urlparse(url)
if url.startswith('https'):
    conn = httplib.HTTPSConnection(o.netloc)
else:
    conn = httplib.HTTPConnection(o.netloc)

if o.query:
    conn.request("HEAD", o.path + '?' + o.query)
else:
    conn.request("HEAD", o.path)

res = conn.getresponse()
print res.status, res.reason, '\n'
print '\n'.join(['%-16s %s' % (k,v) for k,v in res.getheaders()])
