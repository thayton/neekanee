import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Basis Technology',
    'hq': 'Cambridge, MA',

    'benefits': {
        'vacation': [(1,15)],
        'tuition_assistance': True
        },

    'home_page_url': 'http://www.basistech.com',
    'jobs_page_url': 'http://www.basistech.com/careers/',

    'empcnt': [51,200]
}

class BasisTechJobScraper(JobScraper):
    def __init__(self):
        super(BasisTechJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/careers/#')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            i = a['href'].find('#')
            d = s.find('div', id=a['href'][i+1:])

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BasisTechJobScraper()
