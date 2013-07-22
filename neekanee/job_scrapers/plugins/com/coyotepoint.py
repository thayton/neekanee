import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Coyote Point Systems',
    'hq': 'Millerton, NY',

    'home_page_url': 'http://www.coyotepoint.com',
    'jobs_page_url': 'http://www.coyotepoint.com/jobs.php',

    'empcnt': [11,50]
}

class CoyotePointJobScraper(JobScraper):
    def __init__(self):
        super(CoyotePointJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'field-item even', 'property': True}
        d = s.find('div', attrs=x)
        d.extract()

        self.company.job_set.all().delete()

        for g in d.findAll('strong'):
            job = Job(company=self.company)
            job.title = g.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = g.next
            while x:
                if hasattr(x, 'name') is False:
                    job.desc += x
                elif x.name == 'p' and x.text.strip().startswith('_______'):
                    break
                x = x.next

            job.save()

def get_scraper():
    return CoyotePointJobScraper()
