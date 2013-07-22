import sys
import urlutil

from jobscraper import JobScraper
from neekanee_solr.models import *

from django.core.exceptions import ObjectDoesNotExist

def mkurl(company, old_job_link):
    """
    Query portion of the url returned looks like this:
    
    cim_jobdetail.asp?jobId=1212739&siteId=69&partnerid=119

    Full url eg:

    https://sjobs.brassring.com/en/asp/tg/cim_jobdetail.asp?jobId=1212739&siteId=69&partnerid=119
    """
    items = urlutil.url_query_get(company.jobs_page_url, ['partnerid', 'siteid'])

    url = urlutil.url_query_filter(old_job_link, 'jobId')
    url = urlutil.url_query_add(url, items.iteritems())
    
    return url

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <home_page_url>\n' % sys.argv[0])
        sys.exit(1)

    try:
        company = Company.objects.get(home_page_url=sys.argv[1])
    except ObjectDoesNotExist:
        sys.stderr.write('Company with that home page url not found\n')
        sys.exit(1)

    for job in company.job_set.all():
        newurl = mkurl(company, job.url)
        print newurl
        job.url = newurl
        job.save()
