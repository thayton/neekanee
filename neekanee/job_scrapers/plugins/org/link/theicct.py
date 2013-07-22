import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Council on Clean Transportation',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.icct.org',
    'jobs_page_url': 'http://www.theicct.org/jobs',

    'empcnt': [11,50]
}

class IcctJobScraper(JobScraper):
    def __init__(self):
        super(IcctJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = s.find('form', id='views-exposed-form-Jobs-page-1')
        d = f.findParent('div')
        r = re.compile(r'^/job-postings/[^/]+$')

        for a in d.findAll('a', href=r):
            if not a.h2:
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
            d = s.find('div', id='main-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IcctJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
