import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Competitive Enterprise Institute',
    'hq': 'Washington, DC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.cei.org',
    'jobs_page_url': 'http://cei.org/jobs',

    'empcnt': [11,50]
}

class CeiJobScraper(JobScraper):
    def __init__(self):
        super(CeiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Jobs'
        h = s.find(f)
        d = h.findNext('div')
        x = {'style': 'text-align: center;'}

        self.company.job_set.all().delete()

        for p in d.findAll('p', attrs=x):
            job = Job(company=self.company)
            job.title = p.strong.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = p.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'p' and \
                        x.has_key('style') and x['style'] == 'text-align: center;':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return CeiJobScraper()
