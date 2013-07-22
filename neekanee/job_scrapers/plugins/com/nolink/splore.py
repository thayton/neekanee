import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Splore',
    'hq': 'Sunnyvale, CA',

    'home_page_url': 'http://www.splore.com',
    'jobs_page_url': 'http://www.splore.com/content/jobs',

    'empcnt': [11,50]
}

class SploreJobScraper(JobScraper):
    def __init__(self):
        super(SploreJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h1' and x.text == 'Careers at Splore'
        h = s.find(f)
        d = h.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for h3 in d.findAll('h3'):
            job = Job(company=self.company)
            job.title = h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h3.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next
                
            job.save()

def get_scraper():
    return SploreJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
