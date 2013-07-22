import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Expressor Software',
    'hq': 'Burlington, MA',

    'ats': 'Online Form',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.expressor-software.com',
    'jobs_page_url': 'http://www.expressor-software.com/about-careers.htm',

    'empcnt': [11,50]
}

class ExpressorSoftwareJobScraper(JobScraper):
    def __init__(self):
        super(ExpressorSoftwareJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/[\w-]+/about-us-career-detail\.htm$')

        for a in s.findAll('a', href=r):
            if a.text.lower().find("no open positions") != -1:
                continue

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
            t = s.find('td', id='Content')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ExpressorSoftwareJobScraper()

