import re, urlparse, mechanize, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'FireEye',
    'hq': 'Milpitas, CA',

    'ats': 'newton',

    'contact': 'hr@fireeye.com',

    'home_page_url': 'http://www.fireeye.com',
    'jobs_page_url': 'http://newton.newtonsoftware.com/career/CareerHome.action?clientId=8aa00506326e915601326f65b82e1fcb',

    'empcnt': [51,200]
}

class FireEyeJobScraper(JobScraper):
    def __init__(self):
        super(FireEyeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'/career/JobIntroduction\.action\?clientId=')

        for l in self.br.links(url_regex=r):
            job = Job(company=self.company)
            job.title = l.text
            job.url = urlparse.urljoin(self.br.geturl(), l.url)
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
            l = s.find('td', id='gnewtonJobLocation')
            t = l.findParent('table')
            l = l.text.split('Location:')[1]
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return FireEyeJobScraper()
