import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Polus Center',
    'hq': 'Clinton, MA',

    'home_page_url': 'http://www.poluscenter.org',
    'jobs_page_url': 'http://poluscenter.org/employment-opportunities',

    'empcnt': [11,50]
}

class PolusCenterJobScraper(JobScraper):
    def __init__(self):
        super(PolusCenterJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        self.company.job_set.all().delete()

        s = soupify(self.br.response().read())
        p = s.find('p', attrs={'class': 'subhead1'})

        if not p:
            return

        t = p.findParent('td')
        z = {'class': 'subhead2'}
        t.extract()

        for p in t.findAll('p', attrs=z):
            job = Job(company=self.company)
            job.title = p.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = p.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'p' and x['class'] == 'subhead2':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return PolusCenterJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
