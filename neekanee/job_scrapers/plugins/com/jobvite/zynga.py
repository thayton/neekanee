import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Zynga',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.zynga.com',
    'jobs_page_url': 'http://company.zynga.com/about/jobs/us-jobs',

    'empcnt': [501,1000]
}

class ZyngaJobScraper(JobScraper):
    def __init__(self):
        super(ZyngaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/about/jobs/location/\S+\-united\-states$')

        for a in s.findAll('a', href=r):
            l = self.parse_location(a.text)
            if l is None:
                continue

            u = urlparse.urljoin(url, a['href'])

            self.br.open(u)

            x = soupify(self.br.response().read())
            v = {'class': 'title'}

            for h3 in x.findAll('h3', attrs=v):
                job = Job(company=self.company)
                job.title = h3.a.text
                job.url = urlparse.urljoin(self.br.geturl(), h3.a['href'])
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
            d = s.find('div', id='panel-middle')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ZyngaJobScraper()
