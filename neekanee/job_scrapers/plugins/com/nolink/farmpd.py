import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Farm Design, Inc',
    'hq': 'Hollis, NH',

    'home_page_url': 'http://www.farmpd.com',
    'jobs_page_url': 'http://www.farmpd.com/careers/',

    'empcnt': [11,50]
}

class FarmJobScraper(JobScraper):
    def __init__(self):
        super(FarmJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Careers'
        h = s.find(f)
        d = h.findParent('div')
        x = {'class': 'line-sep'}
        d.extract()

        self.company.job_set.all().delete()

        for hr in d.findAll('hr', attrs=x):
            g = hr.findNext('strong')
            x = g

            job = Job(company=self.company)
            job.title = g.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            while x:
                name = getattr(x, 'name', None)
                if name == 'hr':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return FarmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
