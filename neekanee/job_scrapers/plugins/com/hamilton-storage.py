import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hamilton Storage Technologies',
    'hq': 'Hopkinton, MA',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.hamilton-storage.com',
    'jobs_page_url': 'http://www.hamilton-storage.com/storage-technologies/careers/',

    'empcnt': [11,50]
}

class HamiltonStorageJobScraper(JobScraper):
    def __init__(self):
        super(HamiltonStorageJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^storage-technologies/careers/')
        d = { 'href': r, 'class': 'internal-link' }
    
        for a in s.findAll('a', attrs=d):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.company.home_page_url, a['href'])
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
            h = s.find('h1')
            d = h.findParent('div').parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HamiltonStorageJobScraper()
