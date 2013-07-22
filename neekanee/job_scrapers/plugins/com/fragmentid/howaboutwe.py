import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'HowAboutWe',
    'hq': 'New York, NY',

    'contact': 'jobs@howaboutwe.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.howaboutwe.com',
    'jobs_page_url': 'http://www.howaboutwe.com/jobs',

    'empcnt': [1,10]
}

class HowAboutWeJobScraper(JobScraper):
    def __init__(self):
        super(HowAboutWeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Open Positions'
        h2 = s.find(f)
        ul = h2.findNext('ul')
        r = re.compile(r'^/jobs/\S+$')

        for a in ul.findAll('a', href=r):
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
            a = s.find('article')
            d = a.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HowAboutWeJobScraper()
