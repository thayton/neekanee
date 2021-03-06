import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'DataLab USA',
    'hq': 'Germantown, MD',

    'home_page_url': 'http://www.datalabusa.com',
    'jobs_page_url': 'http://www.datalabusa.com/careers',

    'empcnt': [51,200]
}

class DataLabJobScraper(JobScraper):
    def __init__(self):
        super(DataLabJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('article', id='content')
        r = re.compile(r'^/all-careers/\d+')
        f = lambda x: x.name == 'a' and re.search(r, x.get('href', '')) and x.parent.name == 'span'

        for a in d.findAll(f):
            if len(a.text.strip()) == 0:
                continue

            if a.get('title'):
                continue

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
            d = s.find('article', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DataLabJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
