import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Loftware',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.loftware.com',
    'jobs_page_url': 'http://www.loftware.com/company/careers.cfm',

    'empcnt': [51,200]
}

class LoftwareJobScraper(JobScraper):
    def __init__(self):
        super(LoftwareJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='container')
        x = {'name': True, 'id': True}
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            h3 = a.findNext('h3')
            job = Job(company=self.company)
            job.title = h3.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['id'])
            job.location = self.company.location
            job.desc = ''

            x = h3

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.has_key('name'):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return LoftwareJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
