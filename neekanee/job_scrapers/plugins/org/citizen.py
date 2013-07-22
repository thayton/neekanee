import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Public Citizen',
    'hq': 'Washington, DC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.citizen.org',
    'jobs_page_url': 'http://www.citizen.org/jobs/job_index.cfm',

    'empcnt': [51,200]
}

class CitizenJobScraper(JobScraper):
    def __init__(self):
        super(CitizenJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        l = 'http://www.citizen.org/jobs/joblink.cfm?jobno='
        f = s.find('form', attrs={'action': 'job_action.cfm'})

        for o in f.select.findAll('option'):
            job = Job(company=self.company)
            job.title = o.text
            job.url = l + o['value']
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
            d = s.find('div', id='contentSecondaryDetails')
            d = d.find('div', attrs={'class': 'gutter'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CitizenJobScraper()
