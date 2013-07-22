import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bay Microsystems',
    'hq': 'San Jose, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.baymicrosystems.com',
    'jobs_page_url': 'http://www.baymicrosystems.com/careers.php',

    'empcnt': [51,200]
}

class BayMicroJobScraper(JobScraper):
    def __init__(self):
        super(BayMicroJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='container')
        t = d.find(text='Current Openings')
        u = t.findNext('ul')
        r = re.compile(r'^careers_.*\.php$')

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        self.company.ats = 'Online form'

        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='l_col')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BayMicroJobScraper()
