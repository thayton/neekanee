import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Notable Solutions, Inc',
    'hq': 'Rockville, MD',

    'contact': 'careers@nsius.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.nsiautostore.com',
    'jobs_page_url': 'http://www.nsiautostore.com/about-nsi/careers/',

    'empcnt': [51,200]
}

class NsiAutoStoreJobScraper(JobScraper):
    def __init__(self):
        super(NsiAutoStoreJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h4' and x.text == 'Current Listings'
        h = s.find(f)
        d = h.findParent('div')

        self.company.job_set.all().delete()

        for a in d.findAll('a', href='#'):
            m = re.search(r'\((.*)\)$', a.text)
            if not m:
                continue

            l = self.parse_location(m.group(1))
            d = a.findNext('div', attrs={'class': 'toggle_container'})

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NsiAutoStoreJobScraper()
