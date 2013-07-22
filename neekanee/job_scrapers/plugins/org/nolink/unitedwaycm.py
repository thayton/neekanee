import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'United Way of Central Massachusetts',
    'hq': 'Worcester, MA',

    'home_page_url': 'http://www.unitedwaycm.org',
    'jobs_page_url': 'http://www.unitedwaycm.org/index.php/info/career_opportunities/',

    'empcnt': [51,200]
}

class UnitedWayJobScraper(JobScraper):
    def __init__(self):
        super(UnitedWayJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h4' and x.text == 'Open Positions:'
        h = s.find(f)
        d = h.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for h5 in d.findAll('h5'):
            job = Job(company=self.company)
            job.title = h5.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h5.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'h5':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return UnitedWayJobScraper()
        
if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
