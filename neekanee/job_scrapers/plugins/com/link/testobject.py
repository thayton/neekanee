import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'TestObject GmbH',
    'hq': 'Hennigsdorf, Germany',

    'home_page_url': 'http://testobject.com',
    'jobs_page_url': 'http://testobject.com/jobs',

    'empcnt': [11,50]
}

class TestObjectJobScraper(JobScraper):
    def __init__(self):
        super(TestObjectJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'a' and x.text == 'Apply'

        self.company.job_set.all().delete()

        for a in s.findAll(f):
            d = a.findParent('div')
            d = d.findParent('div', id=True)
            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + d['id'])
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TestObjectJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
