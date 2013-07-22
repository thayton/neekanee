import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The Trustees of Reservations',
    'hq': 'Beverly, MA',

    'home_page_url': 'http://www.thetrustees.org',
    'jobs_page_url': 'http://www.thetrustees.org/about-us/employment/current-openings/',

    'empcnt': [201,500]
}

class TheTrusteesJobScraper(JobScraper):
    def __init__(self):
        super(TheTrusteesJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='contentDiv')
        r = re.compile(r'/about-us/employment/current-openings/[\w-]+\.html$')

        for a in d.findAll('a', href=r):
            if len(a.text.strip()) == 0:
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
            d = s.find('div', id='ctrcol')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TheTrusteesJobScraper()
