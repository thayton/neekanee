import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ShoeBuy',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.shoebuy.com',
    'jobs_page_url': 'http://www.shoebuy.com/contact/employment.jsp',

    'empcnt': [51,200]
}

class ShoeBuyJobScraper(JobScraper):
    def __init__(self):
        super(ShoeBuyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        p = s.find('span', attrs={'class': 'anc_text'})
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in p.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find('a', attrs={'name' : a['href'][1:]})
            if not x:
                continue

            x = x.next

            while getattr(x, 'name', None) != 'a':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return ShoeBuyJobScraper()
