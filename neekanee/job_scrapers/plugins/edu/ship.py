import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Shippensburg University',
    'hq': 'Shippensburg, PA',

    'home_page_url': 'http://www.ship.edu',
    'jobs_page_url': 'http://www.ship.edu/HR/Positions/',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class ShipJobScraper(JobScraper):
    def __init__(self):
        super(ShipJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        i = s.find('iframe')

        self.br.open(i['src'])

        s = soupify(self.br.response().read())
        r = re.compile(r'hr-position\.pl\?mode=view&id=\d+')

        for a in s.findAll('a', href=r):
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
            f = s.find('form')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return ShipJobScraper()
