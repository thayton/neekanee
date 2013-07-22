import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'French Institute Alliance Francaise',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.fiaf.org',
    'jobs_page_url': 'http://www.fiaf.org/jobs/index.shtml',

    'empcnt': [51,200]
}

class FiafJobScraper(JobScraper):
    def __init__(self):
        super(FiafJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mainBlock')
        x = {'class': 'CollapsiblePanelContent'}
        d.extract()

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            td = v.findParent('td')

            job = Job(company=self.company)
            job.title = td.p.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return FiafJobScraper()
