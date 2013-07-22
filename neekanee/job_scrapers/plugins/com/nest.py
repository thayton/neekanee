import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nest',
    'hq': 'Palo Alto, CA',

    'ats': 'JobVite',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.nest.com',
    'jobs_page_url': 'http://www.nest.com/careers/',

    'empcnt': [11,50]
}

class NestJobScraper(JobScraper):
    def __init__(self):
        super(NestJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        n = s.find('section', id='jobs')
        x = {'class': 'career-list-section'}
        r = re.compile(r'^/nest-career/')

        for d in n.findAll('div', attrs=x):
            for a in d.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.findPrevious('h5').text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                print job
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        r = re.compile(r'job-detail-content')

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            v = 'right-column-content markdown'
            d = s.find('div', attrs={'class': v})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NestJobScraper()
