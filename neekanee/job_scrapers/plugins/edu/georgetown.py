import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Georgetown University',
    'hq': 'Washington, DC',

    'benefits': {
        'vacation': [(0,21),(1,22),(2,23),(3,24),(4,25),(5,26)],
        'holidays': 13
    },

    'home_page_url': 'http://www.georgetown.edu',
    'jobs_page_url': 'http://www12.georgetown.edu/hr/employment_services/joblist/jobs.cfm',

    'gctw_chronicle': True,

    'empcnt': [5001,10000]
}

class GeorgetownJobScraper(JobScraper):
    def __init__(self):
        super(GeorgetownJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('FormCategory')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'job_description\.cfm\?CategoryID=')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find(text='Job Title: ')
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return GeorgetownJobScraper()
