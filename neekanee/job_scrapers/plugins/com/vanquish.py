import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vanquish',
    'hq': 'Marlborough, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.vanquish.com',
    'jobs_page_url': 'http://www.vanquish.com/job/',

    'empcnt': [1,10]
}

class VanquishJobScraper(JobScraper):
    def __init__(self):
        super(VanquishJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        s = soupify(self.br.response().read())

        for t in s.findAll(text='job description'):
            a = t.parent
            b = t.findPrevious('b')

            job = Job(company=self.company)
            job.title = b.text
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
            h = s.h1

            if h is None:
                t = s.find('table', id='table1')
                t = t.findParent('td')
            else:
                t = h.findNext('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return VanquishJobScraper()
