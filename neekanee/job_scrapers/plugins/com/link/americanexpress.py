import re, urlparse, mechanize, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'American Express',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.americanexpress.com',
    'jobs_page_url': 'https://jobs.americanexpress.com/api/jobs?limit=10&offset=0&page=1',

    'empcnt': [10001]
}

class AmericanExpressJobScraper(JobScraper):
    def __init__(self):
        super(AmericanExpressJobScraper, self).__init__(COMPANY)
        self.br.set_handle_gzip(True)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'),
                              ('Referer',
                               'https://jobs.americanexpress.com/jobs'),
                              ('Accept-Language', 'en-US'),
                              ('Accept', 'application/json, text/plain, */*'),]

#        import sys, logging
#        logger = logging.getLogger("mechanize")
#        logger.addHandler(logging.StreamHandler(sys.stdout))
#        logger.setLevel(logging.DEBUG)
#        self.br.set_debug_http(True)
#        self.br.set_debug_responses(True)
#        self.br.set_debug_redirects(True)

    def scrape_jobs(self):
        self.company.job_set.all().delete()

        self.br.open('https://jobs.americanexpress.com')
        self.br.open('https://jobs.americanexpress.com/api/jasession')
        self.br.open(self.company.jobs_page_url)

        r = self.br.response()
        d = json.loads(r.read())

        for j in d['jobs']:
            l = self.parse_location(j['location'])
            if not l:
                continue
            
            job = Job(company=self.company)
            job.title = j['title']
            job.url = j['apply_url']
            job.location = l
            job.desc = get_all_text(soupify(j['description']))
            job.save()

def get_scraper():
    return AmericanExpressJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    print job_scraper.serialize()
