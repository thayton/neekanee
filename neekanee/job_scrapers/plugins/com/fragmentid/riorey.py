import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'RioRey',
    'hq': 'Bethesda, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.riorey.com',
    'jobs_page_url': 'http://www.riorey.com/company-careers.html',

    'empcnt': [11,50]
}

class RioReyJobScraper(JobScraper):
    def __init__(self):
        super(RioReyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        p = s.find('span', attrs={'class': 'secPara1Resume'})
        p.extract()

        self.company.job_set.all().delete()

        for a in p.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find(attrs={'name' : a['href'][1:]})
            p = x.findNext('p', attrs={'class': 'about'})
            l = p.contents[2].split('Location:')[1]
            l = re.sub(r'USA .*', '', l)
            l = self.parse_location(l)
            x = p

            if l is None:
                continue

            while x and getattr(x, 'name', None) != 'h3':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.location = l
            job.save()

def get_scraper():
    return RioReyJobScraper()
