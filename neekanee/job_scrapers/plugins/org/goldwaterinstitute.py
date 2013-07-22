import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Goldwater Institute',
    'hq': 'Phoenix, AZ',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.goldwaterinstitute.org',
    'jobs_page_url': 'http://www.goldwaterinstitute.org/opportunities-goldwater',

    'empcnt': [11,50]
}

class GoldwaterInstituteJobScraper(JobScraper):
    def __init__(self):
        super(GoldwaterInstituteJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        jobs = []

        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='pageCont')
        x = {'class': 'jobPost'}

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.h4.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

        return jobs


def get_scraper():
    return GoldwaterInstituteJobScraper()
