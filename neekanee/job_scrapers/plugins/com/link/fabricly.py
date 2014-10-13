import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fabricly',
    'hq': 'New York, NY',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.fabricly.com',
    'jobs_page_url': 'http://www.fabricly.com/vacancies',

    'empcnt': [1,10]
}

class FabriclyJobScraper(JobScraper):
    def __init__(self):
        super(FabriclyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())

        ul = s.find('ul', id='positions')
        li = ul.findAll('li')

        f = lambda li: li.has_key('class') == False or li['class'] != 'filled'
        li = filter(f, li)

        for a in [ l.a for l in li ]:
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

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FabriclyJobScraper()