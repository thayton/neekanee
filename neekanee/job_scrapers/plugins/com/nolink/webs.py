import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Webs',
    'hq': 'Silver Spring, MD',

    'home_page_url': 'http://www.webs.com',
    'jobs_page_url': 'http://www.webs.com/Careers/',

    'empcnt': [11,50]
}

class WebsJobScraper(JobScraper):
    def __init__(self):
        super(WebsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = {'class': 'career-listing'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=a):
            x = {'class': 'career-listing-location'}
            l = d.find('span', attrs=x)
        
            if l:
                l = l.b.nextSibling
                l = self.parse_location(l)

                if not l:
                    continue

            r = re.compile(r'career-listing-full-\d+')
            v = d.find('div', id=r)

            job = Job(company=self.company)
            job.title = d.h3.text
            job.location = l
            job.url = self.br.geturl()
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return WebsJobScraper()
