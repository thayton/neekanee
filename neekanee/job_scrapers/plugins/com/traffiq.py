import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Traffiq',
    'hq': 'New York, NY',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.traffiq.com',
    'jobs_page_url': 'http://www.traffiq.com/contact',

    'empcnt': [11,50]
}

class TraffiqJobScraper(JobScraper):
    def __init__(self):
        super(TraffiqJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'careers'}
        r = re.compile(r'^/careers/')

        for u in s.findAll('ul', attrs=x):
            for a in u.findAll('a', href=r):
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
            d = s.find('div', attrs={'class': 'box_content sexy_gradient'})

            job.desc = get_all_text(d.div)
            job.save()

def get_scraper():
    return TraffiqJobScraper()
