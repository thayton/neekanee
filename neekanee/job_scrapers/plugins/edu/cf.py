import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'College of Central Florida',
    'hq': 'Ocala, FL',

    'benefits': {
        'url': 'http://www.cf.edu/departments/admin/hr/benefits.htm',
        'vacation': [(0,12),(6,15),(11,18)],
        'holidays': 13
    },

    'home_page_url': 'http://www.cf.edu',
    'jobs_page_url': 'https://hrapps2.cf.edu/list_jobopenings.php?cat=all',

    'empcnt': [201,500]
}

class CfJobScraper(JobScraper):
    def __init__(self):
        super(CfJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = { 'class': 'jobtable' }

        self.company.job_set.all().delete()

        for t in s.findAll('table', attrs=d):
            h = t.find(attrs={'abbr': 'Job Title'})
            job = Job(company=self.company)
            job.title = h.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CfJobScraper()
