import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'thredUP',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.thredup.com',
    'jobs_page_url': 'http://www.thredup.com/about/jobs',

    'empcnt': [11,50]
}

class ThredUpJobScraper(JobScraper):
    def __init__(self):
        super(ThredUpJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        p = s.h3.findNext('p')
        d = p.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for a in p.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(attrs={'id' : a['href'][1:]})
            x = x.next

            while x and getattr(x, 'name', None) != 'h2':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return ThredUpJobScraper()
