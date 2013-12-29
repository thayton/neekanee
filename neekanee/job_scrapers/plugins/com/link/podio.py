import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Podio',
    'hq': 'Copenhagen, Denmark',

    'home_page_url': 'https://company.podio.com',
    'jobs_page_url': 'https://company.podio.com/jobs',

    'empcnt': [11,50]
}

class PodioJobScraper(JobScraper):
    def __init__(self):
        super(PodioJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs'}
        y = {'class': 'locations'}
        r = re.compile(r'^/jobs/[^/]+$')

        for u in s.findAll('ul', attrs=x):
            p = u.findParent('ul', attrs=y)
            l = self.parse_location(p.strong.text)

            if not l:
                continue

            for a in u.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
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
            x = {'class': 'show-job'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PodioJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
