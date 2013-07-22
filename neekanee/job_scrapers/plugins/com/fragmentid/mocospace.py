import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MocoSpace',
    'hq': 'Boston, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.mocospace.com',
    'jobs_page_url': 'http://www.jnjmobile.com/jobs.jsp',

    'empcnt': [11,50]
}

class MocoSpaceJobScraper(JobScraper):
    def __init__(self):
        super(MocoSpaceJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        u = s.h3.findNext('ul')
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find(attrs={'name' : a['href'][1:]})
            x = x.next

            while getattr(x, 'name', None) != 'hr':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return MocoSpaceJobScraper()
