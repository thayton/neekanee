import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Epilepsy Foundation',
    'hq': 'Landover, MD',

    'home_page_url': 'http://www.epilepsyfoundation.org',
    'jobs_page_url': 'http://www.epilepsyfoundation.org/careers.cfm',

    'empcnt': [51,200]
}

class EpilepsyFoundationJobScraper(JobScraper):
    def __init__(self):
        super(EpilepsyFoundationJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'CP___PAGEID=\d+,\S+\.cfm,\d+|')

        for a in s.findAll('a', id=r):
            if len(a.text) > 0:
                continue

            title = a.findParent('p').text
            if title == 'benefits':
                continue

            job = Job(company=self.company)
            job.title = title
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

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EpilepsyFoundationJobScraper()
