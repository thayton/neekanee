import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'SitScape',
    'hq': 'Tysons Corner, VA',

    'contact': 'jobs@sitscape.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.sitscape.com',
    'jobs_page_url': 'http://www.sitscape.com/aboutus/career.html',

    'empcnt': [11,50]
}

class SitScapeJobScraper(JobScraper):
    def __init__(self):
        super(SitScapeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        u = s.ul
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find(attrs={'name' : a['href'][1:]})
            x = x.parent.findNextSibling('h6')

            l = self.parse_location(x.text)
            if not l:
                continue

            job.location = l
                
            while x is not None and getattr(x, 'name', None) != 'h4':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return SitScapeJobScraper()
