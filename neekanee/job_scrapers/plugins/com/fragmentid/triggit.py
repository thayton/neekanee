import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Triggit',
    'hq': 'San Francisco, CA',

    'contact': 'jobs@triggit.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://triggit.com',
    'jobs_page_url': 'http://triggit.com/careers/',

    'empcnt': [11,50]
}

class TriggitJobScraper(JobScraper):
    def __init__(self):
        super(TriggitJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        u = s.find('ul', id='career_section_list')
        r = re.compile(r'^#\S+_\d+$')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find(attrs={'name' : a['href'][1:]})
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
    return TriggitJobScraper()
