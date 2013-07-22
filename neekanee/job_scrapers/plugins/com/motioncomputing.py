import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Motion Computing',
    'hq': 'Austin, TX',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.motioncomputing.com',
    'jobs_page_url': 'http://www.motioncomputing.com/about/careers.asp',

    'empcnt': [201,500]
}

class MotionComputingJobScraper(JobScraper):
    def __init__(self):
        super(MotionComputingJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^jobs/')

        for a in s.findAll('a', href=r):
            t = a.findNext(text=' - ')

            if t is None: 
                continue

            t = t.findNext(text=True)
            l = self.parse_location(t)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='one_column')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MotionComputingJobScraper()
