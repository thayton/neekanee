#!/usr/bin/env python

import sys
import getopt
import mechanize

from BeautifulSoup import BeautifulSoup

def usage():
    sys.stderr.write('usage: upload_job -u <url> -f <file>\n')

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:f:")
    except getopt.GetoptError, err:
        print str(err) 
        usage()
        sys.exit(1)

    url = None
    file = None

    for opt, val in opts:
        if opt == "-u":
            url = val
        elif opt == "-f":
            file = val
        else:
            assert False, "unhandled option"

    if not url or not file:
        usage()
        sys.exit(1)

    print 'url=%s' % url
    print 'file=%s' % file

    with open(file) as f:
        br = mechanize.Browser()
        br.open(url)
        br.select_form('upload_jobs')
        br.add_file(filename=file, file_object=f)
        br.submit()
        print br.response().read()
