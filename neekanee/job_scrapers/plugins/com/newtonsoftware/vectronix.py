import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vectronix',
    'hq': 'Leesburg, VA',

    'ats': 'newton',

    'home_page_url': 'http://www.vectronix.us/html/',
    'jobs_page_url': 'http://newton.newtonsoftware.com/career/CareerHome.action?clientId=4028f88b2c2b3e87012c2c8918a704a9',

    'empcnt': [11,50]
}

class VectronixJobScraper(JobScraper):
    def __init__(self):
        super(VectronixJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'/career/JobIntroduction\.action\?clientId=')
        for l in self.br.links(url_regex=r):
            job = Job(company=self.company)
            job.title = l.text
            job.url = l.url
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
    return VectronixJobScraper()
