import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Care.com',
    'hq': 'Waltham, MA',

    'contact': 'careers@care.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.care.com',
    'jobs_page_url': 'http://www.care.com/careers-p1089.html',

    'empcnt': [51,200],
}

class CareJobScraper(JobScraper):
    def __init__(self):
        super(CareJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', attrs={'class': 'careers'})
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            if a.parent.name != 'li':
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.desc = ''

            x = d.find(attrs={'name' : a['href'][1:]})

            if not x:
                continue

            x = x.next
            
            b = x.findNext('br')
            l = self.parse_location(b.next)

            if l is None:
                continue

            job.location = l

            while x and getattr(x, 'name', None) != 'hr':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next
        
            job.save()

def get_scraper():
    return CareJobScraper()

