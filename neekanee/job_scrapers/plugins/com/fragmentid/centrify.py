import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Centrify',
    'hq': 'Sunnyvale, CA',

    'contact': 'jobs@centrify.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.centrify.com',
    'jobs_page_url': 'http://www.centrify.com/aboutcentrify/jobs.asp',

    'empcnt': [51,200]
}

class CentrifyJobScraper(JobScraper):
    def __init__(self):
        super(CentrifyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', id='page_content')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.table.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = td[-1].text
            l = re.sub(r', USA', '', l)
            l = self.parse_location(l)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.desc = ''

            x = d.find('h2', id=a['href'][1:])
            x = x.next

            while x and getattr(x, 'name', None) != 'h2':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.location = l
            job.save()

def get_scraper():
    return CentrifyJobScraper()
