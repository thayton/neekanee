import re, urllib2, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Pop*Art',
    'hq': 'Portland, OR',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.popart.com',
    'jobs_page_url': 'http://www.popart.com/company/careers/default.aspx',

    'empcnt': [11,50]
}

class PopArtJobScraper(JobScraper):
    def __init__(self):
        super(PopArtJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'open-positions'}
        d = s.find('div', attrs=x)
        r = re.compile(r'^/company/careers/')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.location = self.company.location
            job.url = urlparse.urljoin(self.br.geturl(), urllib2.quote(a['href']))
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'description'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PopArtJobScraper()
