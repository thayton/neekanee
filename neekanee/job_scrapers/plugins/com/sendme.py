import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'SendMe',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.sendme.com',
    'jobs_page_url': 'http://www.sendme.com/careers/',

    'empcnt': [51,200]
}

class SendMeJobScraper(JobScraper):
    def __init__(self):
        super(SendMeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        v = {'class': 'career_available_header'}
        d = s.find('div', attrs=v)
        u = d.findNext('ul')
        r = re.compile(r'^/careers/.*\.html$')

        for a in u.findAll('a', href=r):
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
            d = s.find('div', id='main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SendMeJobScraper()
