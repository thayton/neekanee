import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'DPR Construction',
    'hq': 'Redwood City, CA',

    'home_page_url': 'http://www.dpr.com',
    'jobs_page_url': 'http://www.dpr.com/company/careers/current-positions',

    'empcnt': [1001,5000]
}

class DprJobScraper(JobScraper):
    def __init__(self):
        super(DprJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'/company/careers/current-positions/[a-z-]+$')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')
            l = d.h3.text.lower()

            if not l.startswith('location:') or d.h3.a is None:
                continue

            l = self.parse_location(d.h3.a.text)
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DprJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
