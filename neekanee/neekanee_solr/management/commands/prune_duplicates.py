import sys
import urlutil

from jobscraper import JobScraper
from neekanee_solr.models import *

from django.core.exceptions import ObjectDoesNotExist

if len(sys.argv) != 2:
    sys.stderr.write('usage: %s <home_page_url>\n' % sys.argv[0])
    sys.exit(1)

try:
    company = Company.objects.get(home_page_url=sys.argv[1])
except ObjectDoesNotExist:
    sys.stderr.write('Company with that home page url not found\n')
    sys.exit(1)

ndups = 0

prunelist = []

print '# jobs: ', company.job_set.count()

for job in company.job_set.all():
    jobs = company.job_set.filter(url=job.url)
    if len(jobs) > 1:
        ndups += 1
        print "Duplicate entries"
        for x in jobs:
            print x.id, x.title, x.url
        job.delete()

print '# duplicates ', ndups
