import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wingspan',
    'hq': 'Blue Bell, PA',

    'ats': 'Online Form',

    'benefits': {
        'vacation': [],
        'holidays': 10
    },

    'home_page_url': 'http://www.wingspan.com',
    'jobs_page_url': 'http://www.wingspan.com/about/careers/',

    'empcnt': [11,50]
}

class WingSpanJobScraper(JobScraper):
    def __init__(self):
        super(WingSpanJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#\d+$')
        d = s.find('div', id='content')
        d = d.find('div', attrs={'class': 'entry-content'})
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
                if name == 'a' and x.get('name', None):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return WingSpanJobScraper()

