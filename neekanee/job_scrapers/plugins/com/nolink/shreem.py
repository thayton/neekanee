import re

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Shreem',
    'hq': 'Sterling, VA',

    'contact': 'recruiting@shreem.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.shreem.com',
    'jobs_page_url': 'http://www.shreem.com/open_positions.htm',

    'empcnt': [11,50]
}

class ShreemJobScraper(JobScraper):
    def __init__(self):
        super(ShreemJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        b = s.html.b
        p = b.parent.parent

        self.company.job_set.all().delete()

        job = Job(company=self.company)
        job.title = b.text
        job.url = self.br.geturl()
        job.location = self.company.location
        job.desc = get_all_text(p)
        job.save()

def get_scraper():
    return ShreemJobScraper()
