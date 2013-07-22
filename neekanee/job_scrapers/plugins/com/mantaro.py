import re

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mantaro Networks, Inc',
    'hq': 'Germantown, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.mantaro.com',
    'jobs_page_url': 'http://www.mantaro.com/aboutus/careers.htm',

    'empcnt': [11,50]
}

class MantaroJobScraper(JobScraper):
    def __init__(self):
        super(MantaroJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        ul = s.html.h1.parent.ul
        li = ul.li

        self.company.job_set.all().delete()

        while li is not None:
            job = Job(company=self.company)
            job.title = li.text
            job.url = self.br.geturl()
            job.location = self.company.location

            ul = li.findNext('ul')
            li = li.findNextSibling('li')

            job.desc = get_all_text(ul)
            job.save()

def get_scraper():
    return MantaroJobScraper()
