import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'University of Maryland Eastern Shore',
    'hq': 'Princess Anne, MD',

    'home_page_url': 'http://www.umes.edu',
    'jobs_page_url': 'http://www.umes.edu/HR/JobBoard.aspx',

    'empcnt': [1001,5000]
}

class UmesJobScraper(JobScraper):
    def __init__(self):
        super(UmesJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/HR/JobArticle\.aspx\?id=\d+$')

        for a in s.findAll('a', href=r):
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
            r = re.compile(r'_lblJobTitle')
            p = s.find('span', id=r)
            t = p.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return UmesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
