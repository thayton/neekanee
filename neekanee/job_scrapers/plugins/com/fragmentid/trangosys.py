import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Trango Systems',
    'hq': 'San Diego, CA',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
     },

    'home_page_url': 'http://www.trangosys.com',
    'jobs_page_url': 'http://www.trangosys.com/about-trango/careers/open-positions.shtml',

    'empcnt': [51,200]
}

class TrangoSysJobScraper(JobScraper):
    def __init__(self):
        super(TrangoSysJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', id='mainContent')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            v = {'name' : a['href'][1:]}
            x = d.find(attrs=v)

            job = Job(company=self.company)
            job.title = x.parent.span.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = x.next
            hr = x.findNext('hr')

            while x and x != hr:
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return TrangoSysJobScraper()
