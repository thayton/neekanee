#!/usr/bin/env python

"""
As a starting point for company overviews, we use a site's meta description
to give some information as to what the company does.
"""

import os, sys, mechanize

from BeautifulSoup import BeautifulSoup

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *

if __name__ == '__main__':
    br = mechanize.Browser()
    br.set_handle_robots(False)

    for company in Company.objects.all():
        if len(company.description) == 0:
            print 'Company %s has an empty description' % company.name
            print 'Retrieving meta description (%s)...' % company.home_page_url

            try:
                br.open(company.home_page_url)
            except:
                print 'Exception encountered opening %s - skipping' % company.home_page_url
                continue

            s = BeautifulSoup(br.response().read())
            x = {'name': 'description', 'content': True}
            m = s.find('meta', attrs=x)

            if not m:
                print 'No meta description tag...'
                continue

            print 'Meta description for %s' % company.name
            print m['content']

            company.description = m['content']
            company.save()
