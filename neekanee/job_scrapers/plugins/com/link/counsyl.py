import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Counsyl',
    'hq': 'San Francisco, CA',

    'home_page_url': 'https://www.counsyl.com',
    'jobs_page_url': 'https://www.counsyl.com/jobs/',

    'empcnt': [51,200]
}

class CounsylJobScraper(JobScraper):
    def __init__(self):
        super(CounsylJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'joblist'}
        r = re.compile(r'^/jobs/[^/]+/$')
        
        for u in s.findAll('ul', attrs=x):
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

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')
            r = re.compile(r'^Location:')
            t = d.find(text=r)
            if t:
                l = re.sub(r, '', t)
                l = self.parse_location(l)
                if l:
                    job.location = l

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CounsylJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
