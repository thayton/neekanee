import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Listia',
    'hq': 'San Jose, CA',

    'contact': 'jobs@listia.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.listia.com',
    'jobs_page_url': 'http://www.listia.com/jobs',

    'empcnt': [1,10]
}

class ListiaJobScraper(JobScraper):
    def __init__(self):
        super(ListiaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'section_title'}

        self.company.job_set.all().delete()

        for h2 in s.findAll('h2', attrs=x):
            d = h2.findParent('div', attrs={'class': 'gray_box'})
            if not d:
                continue

            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.desc = get_all_text(d)
            job.location = self.company.location
            job.save()

def get_scraper():
    return ListiaJobScraper()
