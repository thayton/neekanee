import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Net Impact',
    'hq': 'Boston, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.netimpact.org',
    'jobs_page_url': 'http://netimpact.org/about/employment',

    'empcnt': [11,50]
}

class NetImpactJobScraper(JobScraper):
    def __init__(self):
        super(NetImpactJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/about/employment/employment/#')
        d = s.find('div', id='content-core')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            if a['href'].lower().endswith('#top'):
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            i = a['href'].find('#')
            x = d.find(attrs={'name' : a['href'][i+1:]})

            while x:
                name = getattr(x, 'name', None)
                if name == 'hr':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return NetImpactJobScraper()
