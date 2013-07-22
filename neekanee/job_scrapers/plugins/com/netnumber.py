import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'NetNumber',
    'hq': 'Lowell, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.netnumber.com',
    'jobs_page_url': 'http://www.netnumber.com/about-us-employment.htm',

    'empcnt': [11,50]
}

class NetNumberJobScraper(JobScraper):
    def __init__(self):
        super(NetNumberJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('td', id='content')
        r = re.compile(r'^/[a-zA-Z0-9-]+/about-us-job-detail.htm')

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(url, a['href'])
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
            d = s.find('td', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NetNumberJobScraper()
