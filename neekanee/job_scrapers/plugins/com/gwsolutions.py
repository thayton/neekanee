import re

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Global Wireless Solutions',
    'hq': 'Dulles, VA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.gwsolutions.com',
    'jobs_page_url': 'http://www.gwsolutions.com/careers.html',

    'empcnt': [51,200]
}

class GwSolutionsJobScraper(JobScraper):
    def __init__(self):
        super(GwSolutionsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = {'class': 'style128'}

        self.company.job_set.all().delete()

        for p in s.findAll('p', attrs=d):
            if p.span is None:
                job = Job(company=self.company)
                job.title = p.contents[0].strip()
                job.url = self.br.geturl()
                job.location = self.company.location

                b = p.findNext('blockquote')

                job.desc = get_all_text(b)
                job.save()

def get_scraper():
    return GwSolutionsJobScraper()

