import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Robert Wood Johnson Foundation',
    'hq': 'Princeton, NJ',

    'home_page_url': 'http://www.rwjf.org',
    'jobs_page_url': 'http://www.rwjf.org/en/about-rwjf/job-opportunities.html',

    'empcnt': [201,500]
}

class RwjfJobScraper(JobScraper):
    def __init__(self):
        super(RwjfJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/en/about-rwjf/job-opportunities/[a-z-]+\.html$')
        x = {'class': 'freeform'}
        c = s.find('article', attrs=x)
        d = c.parent

        for a in d.findAll('a', href=r):
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
            x = {'class': 'freeform'}
            a = s.find('article', attrs=x)

            job.desc = get_all_text(a.parent)
            job.save()

def get_scraper():
    return RwjfJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
