import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sociomantic',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.sociomantic.com',
    'jobs_page_url': 'http://careers.sociomantic.com',

    'empcnt': [11,50]
}

class SociomanticJobScraper(JobScraper):
    def __init__(self):
        super(SociomanticJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-list__job--link'}
        y = {'data-location': True}

        for a in s.findAll('a', attrs=x):
            p = a.find('span', attrs=y)
            l = self.parse_location(p.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.span.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            a = s.find('article')

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return SociomanticJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
