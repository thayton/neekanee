import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Photojojo',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://photojojo.com',
    'jobs_page_url': 'http://photojojo.com/jobs/',

    'empcnt': [1,10]
}

class PhotoJojoJobScraper(JobScraper):
    def __init__(self):
        super(PhotoJojoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-summary'}
        r = re.compile(r'\S+\.html$')

        for d in s.findAll('div', attrs=x):
            if not re.search(r, d.a['href']):
                continue

            job = Job(company=self.company)
            job.title = d.a.text
            job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
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
            a = {'class': 'nofadeout'}
            d = s.find('div', attrs=a)

            if d is None:
                d = s.div

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PhotoJojoJobScraper()
