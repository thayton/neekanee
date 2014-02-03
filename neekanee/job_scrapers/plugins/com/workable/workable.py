import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Workable',
    'hq': 'Attiki, Greece',

    'home_page_url': 'http://workable.com',
    'jobs_page_url': 'http://careers.workable.com',

    'empcnt': [11,50]
}

class WorkableJobScraper(JobScraper):
    def __init__(self):
        super(WorkableJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/jobs/\d+$')

        for a in s.findAll('a', href=r):
            li = a.findParent('li')
            t = li.p.text
            l = self.parse_location(t.split('&middot;')[0])

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
            m = s.find('main', id='main')

            job.desc = get_all_text(m)
            job.save()

def get_scraper():
    return WorkableJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
