import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ReadMore',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'http://readmo.re/',
    'jobs_page_url': 'http://readmo.re/jobs.html',

    'empcnt': [1,10]
}

class ReadmoJobScraper(JobScraper):
    def __init__(self):
        super(ReadmoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^Apply')
        f = lambda x: x.name == 'a' and re.search(r, x.text)

        self.company.job_set.all().delete()

        for a in s.findAll(f):
            n = a.findParent('section')
            job = Job(company=self.company)
            job.title = n.h2.contents[0]
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return ReadmoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
