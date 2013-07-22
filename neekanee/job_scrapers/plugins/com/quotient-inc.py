import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Quotient',
    'hq': 'Columbia, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.quotient-inc.com',
    'jobs_page_url': 'http://www.quotient-inc.com/careers',

    'empcnt': [51,200]
}

class QuotientIncJobScraper(JobScraper):
    def __init__(self):
        super(QuotientIncJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'careers-listing'})
        r = re.compile(r'^/careers/')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            h = s.html.h1
            d = h.parent.parent

            l = d.find(text='Location')
            l = l.findNext(text=True)
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return QuotientIncJobScraper()
