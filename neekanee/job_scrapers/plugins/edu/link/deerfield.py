import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Deerfield Academy',
    'hq': 'Springfield, MA',

    'home_page_url': 'http://deerfield.edu',
    'jobs_page_url': 'http://deerfield.edu/jobs',

    'empcnt': [51,200]
}

class DeerfieldJobScraper(JobScraper):
    def __init__(self):
        super(DeerfieldJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        # HTML is broken - skipped past to just the <body>
        d = self.br.response().read()
        i = d.find('<body')
        s = soupify(d[i:])
        x = {'class': 'posts-list'}
        u = s.find('ul', attrs=x)
        r = re.compile(r'^/job/[^/]+/$')

        for a in u.findAll('a', href=r):
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

            # HTML is broken - skipped past to just the <body>
            d = self.br.response().read()
            i = d.find('<body')
            s = soupify(d[i:])

            r = re.compile(r'^/job/[^/]+/$')
            a = s.find('a', href=r)
            d = a.findParent('div', id='content_lc')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DeerfieldJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
