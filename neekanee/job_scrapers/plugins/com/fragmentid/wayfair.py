import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'WayFair',
    'hq': 'Boston, MA',

    'benefits': {'vacation': [(0,15)]},

    'home_page_url': 'http://www.wayfair.com',
    'jobs_page_url': 'http://www.wayfair.com/careers#section=opportunities',

    'empcnt': [501,1000]
}

class WayFairJobScraper(JobScraper):
    def __init__(self):
        super(WayFairJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobRow'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            v = {'class': 'jobLocation'}
            p = d.find('span', attrs=v)
            l = self.parse_location(p.text)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = d.a.text
            job.url = urlparse.urljoin(self.br.geturl(), '#job=%s' % d.a['data-id'])
            job.location = l

            v = s.find('div', id=d.a['data-id'])

            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return WayFairJobScraper()
