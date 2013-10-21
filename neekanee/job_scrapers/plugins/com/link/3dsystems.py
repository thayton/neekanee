import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '3D Systems',
    'hq': 'Rock Hill, SC',

    'home_page_url': 'http://www.3dsystems.com',
    'jobs_page_url': 'http://www.3dsystems.com/careers',

    'empcnt': [501,1000]
}

class SystemsJobScraper(JobScraper):
    def __init__(self):
        super(SystemsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/careers/[^/]+/[\d-]+$')
        
        for a in s.findAll('a', href=r):
            l = a.text.rsplit('-', 1)
            if len(l) < 2:
                continue

            l = self.parse_location(l[1])
            if not l:
                continue

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
            d = s.find('div', id='block-system-main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SystemsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
