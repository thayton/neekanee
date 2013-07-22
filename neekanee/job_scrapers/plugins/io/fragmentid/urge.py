import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Urge IO',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://urge.io',
    'jobs_page_url': 'http://urge.io/jobs',

    'empcnt': [11,50]
}

class UrgeJobScraper(JobScraper):
    def __init__(self):
        super(UrgeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', attrs={'class': 'container'})
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(attrs={'name' : a['href'][1:]})
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += ' ' + x
                x = x.next

            job.save()

def get_scraper():
    return UrgeJobScraper()
