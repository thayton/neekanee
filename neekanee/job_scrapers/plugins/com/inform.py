import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Inform',
    'hq': 'New York, NY',

    'benefits': {'vacation': []},

    'home_page_url': 'http://inform.com',
    'jobs_page_url': 'http://inform.com/jobs.html',

    'empcnt': [11,50]
}

class InformJobScraper(JobScraper):
    def __init__(self):
        super(InformJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        d = d.find('div', attrs={'class': 'main'})
        r = re.compile(r'^job-\d+$')

        self.company.job_set.all().delete()

        for v in d.findAll('div', id=r):
            job = Job(company=self.company)
            job.title = v.strong.text
            job.url = self.br.geturl()
            job.desc = get_all_text(v)
            job.location = self.company.location
            job.save()

def get_scraper():
    return InformJobScraper()
