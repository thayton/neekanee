import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Public Library of Science',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.plos.org',
    'jobs_page_url': 'http://www.plos.org/about/jobs/',

    'empcnt': [51,200]
}

class PlosJobScraper(JobScraper):
    def __init__(self):
        super(PlosJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'entry-content'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/about/jobs/#')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            i = a['href'].find('#')
            y = d.find('a', attrs={'name' : a['href'][i+1:]})
            
            if not y:
                continue

            x = y.findNext('h3')

            if not x:
                x = y.findNext('h2')

            if not x:
                continue

            x = x.next
            while x and getattr(x, 'name', None) != 'h3':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return PlosJobScraper()
