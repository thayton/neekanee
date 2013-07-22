import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Search Optics',
    'hq': 'San Diego, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.searchoptics.com',
    'jobs_page_url': 'http://www.searchoptics.com/company/careers',

    'empcnt': [11,50]
}

class SearchOpticsJobScraper(JobScraper):
    def __init__(self):
        super(SearchOpticsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = {'class': 'jobblock'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=a):
            l = d.h2.br.next.split('Location:')[1]
            l = self.parse_location(l)

            if l is None:
                continue

            z = {'class': 'body'}
            x = d.find('div', attrs=z)

            job = Job(company=self.company)
            job.title = d.h1.text
            job.location = l
            job.url = self.br.geturl()
            job.desc = get_all_text(x)
            job.save()

def get_scraper():
    return SearchOpticsJobScraper()

