import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'LetsLunch',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://letslunch.com',
    'jobs_page_url': 'http://letslunch.com/we-are-hiring',

    'empcnt': [1,10]
}

class LetsLunchJobScraper(JobScraper):
    def __init__(self):
        super(LetsLunchJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='jobs-wrapper')

        self.company.job_set.all().delete()

        for h2 in d.findAll('h2'):
            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h2.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += x
                x = x.next
                
            job.save()

def get_scraper():
    return LetsLunchJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
