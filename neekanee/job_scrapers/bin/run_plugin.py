#!/usr/bin/env python

import os, sys, imp, json, getopt

#sys.path.append(os.path.join(os.path.dirname(__file__), '/Users/thayton/Projects/Mine/'))
#sys.path.append(os.path.join(os.path.dirname(__file__), '/Users/thayton/Projects/Mine/jobsearch/'))

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../jobsearch/'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from neekanee_solr.models import *

def usage():
    sys.stderr.write('usage: run_plugin [-c|-s|-p] <file>\n')
    
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "csp")
    except getopt.GetoptError, err:
        print str(err) 
        usage()
        sys.exit(1)

    scrape_jobs = False
    prune_jobs = False
    clear_jobs = False
    path = None

    for opt, val in opts:
        if opt == "-s":
            scrape_jobs = True
        elif opt == "-p":
            prune_jobs = True
        elif opt == "-c":
            clear_jobs = True
        else:
            assert False, "unhandled option"

    if len(args) == 0 or (not scrape_jobs and not prune_jobs and not clear_jobs):
        usage()
        sys.exit(1)

    path = args[0]

    modname = os.path.splitext(os.path.basename(path))[0]
    plug = imp.load_source(modname, path)

    c = plug.COMPANY
    c['jobs'] = []

    if clear_jobs:
        job_scraper = plug.get_scraper()
        job_scraper.company.job_set.all().delete()

    if scrape_jobs:
        if hasattr(plug, 'get_scraper'):
            job_scraper = plug.get_scraper()

            if hasattr(job_scraper, 'company'):
                job_scraper.scrape_jobs()
                print job_scraper.serialize()
            else:
                job_scraper.scrape_jobs(c)
                print json.dumps(c, indent=4)


    if prune_jobs:
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
