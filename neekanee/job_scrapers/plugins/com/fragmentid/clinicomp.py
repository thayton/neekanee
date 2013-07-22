import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'CliniComp',
    'hq': 'San Diego, CA',

    'contact': 'jobs@clinicomp.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.clinicomp.com',
    'jobs_page_url': 'http://www.clinicomp.com/company/careers.htm',

    'empcnt': [51,200]
}

class CliniCompJobScraper(JobScraper):
    def __init__(self):
        super(CliniCompJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        u = s.ul
        t = u.findParent('td')
        t.extract()

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = t.find('a', attrs={'name' : a['href'][1:]})
            x = x.next.findNext('p')

            while x and getattr(x, 'name', None) != 'h3':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return CliniCompJobScraper()
