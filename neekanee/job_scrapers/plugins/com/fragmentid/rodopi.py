import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rodopi Software',
    'hq': 'San Diego, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.rodopi.com',
    'jobs_page_url': 'http://www.rodopi.com/index.php?page=607',

    'empcnt': [11,50]
}

class RodopiJobScraper(JobScraper):
    def __init__(self):
        super(RodopiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        t = s.find('td', id='content')
        t.extract()

        self.company.job_set.all().delete()

        for a in t.findAll('a', href=r):
            if a['href'] == '#top':
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = t.find(attrs={'name' : a['href'][1:]})
            v = x.findNext('hr')

            while x and x != v:
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return RodopiJobScraper()
