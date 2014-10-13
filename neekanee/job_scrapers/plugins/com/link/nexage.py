import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nexage',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://www.nexage.com',
    'jobs_page_url': 'http://www.nexage.com/careers/job-listings/',

    'empcnt': [11,50]
}

class NexageJobScraper(JobScraper):
    def __init__(self):
        super(NexageJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'box'}

        for b in s.findAll('article', attrs=x):
            l = self.parse_location(b.p.contents[0])
            if not l:
                continue

            job = Job(company=self.company)
            job.title = b.h4.text
            job.url = urlparse.urljoin(self.br.geturl(), b.a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.h1.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NexageJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
