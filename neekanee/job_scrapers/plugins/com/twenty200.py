import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '20x200',
    'hq': 'New York, NY',

    'contact': 'jobs@jenbekman.com', 
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.20x200.com',
    'jobs_page_url': 'http://www.20x200.com/jobs/',

    'empcnt': [11,50]
}

class Twenty200JobScraper(JobScraper):
    def __init__(self):
        super(Twenty200JobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = {'class': 'post-more-link'}

        for a in [ p.a for p in s.findAll('p', attrs=t) ]:
            b = a.findPrevious('b')

            job = Job(company=self.company)
            job.title = b.text
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
            d = s.find('div', attrs={'class': 'rightcolumn'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return Twenty200JobScraper()
        
