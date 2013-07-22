import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'RethinkDB',
    'hq': 'Mountain View, CA',

    'contact': 'jobs@rethinkdb.com',
    'benefits': {'vacation': [(1,20)]},

    'home_page_url': 'http://www.rethinkdb.com',
    'jobs_page_url': 'http://rethinkdb.com/jobs/',

    'empcnt': [1,10]
}

class RethinkDbJobScraper(JobScraper):
    def __init__(self):
        super(RethinkDbJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = {'class': 'position'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=a):
            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + d.a['name'])
            job.desc = get_all_text(d)
            job.location = self.company.location
            job.save()

def get_scraper():
    return RethinkDbJobScraper()
