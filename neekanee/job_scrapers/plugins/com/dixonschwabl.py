import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dixon Schwabl',
    'hq': 'Victor, NY',

    'ats': 'Online Form',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.dixonschwabl.com',
    'jobs_page_url': 'http://dixonschwabl.com/opportunities/job-openings',

    'empcnt': [51,200]
}

class DixonSchwablJobScraper(JobScraper):
    def __init__(self):
        super(DixonSchwablJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        v = d.find('div', attrs={'class': 'view-content'})
        r = re.compile(r'views-row')
        x = {'class': r}

        self.company.job_set.all().delete()

        for d in v.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = self.br.geturl()
            job.location = self.company.location

            n = d.find('div', attrs={'class': 'content'})

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return DixonSchwablJobScraper()

