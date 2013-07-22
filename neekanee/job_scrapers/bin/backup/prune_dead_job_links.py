#!/usr/bin/env python

######################################################################
# Run prune_jobs() method for each plugin that has this method defined
######################################################################

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from neekanee_solr.models import *
from loader import PluginLoader

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <plugin_dir>\n' % sys.argv[0])
        sys.exit(1)

    pldr = PluginLoader()
    pldr.load_plugins([sys.argv[1]])
    
    print 'Loaded %d plugins' % len(pldr.plugins)

    for plug in pldr.plugins:
        if hasattr(plug, 'get_scraper'):
            job_scraper = plug.get_scraper()
            if hasattr(job_scraper, 'prune_jobs'):
                try:
                    company = Company.objects.get(home_page_url=plug.COMPANY['home_page_url'])
                except Company.DoesNotExist:
                    pass
                else:
                    print 'Running %s.prune_jobs' % plug.__name__
                    job_scraper.prune_jobs(company)
