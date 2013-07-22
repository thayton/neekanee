import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'ASI',
    'hq': 'Silver Spring, MD',

    'contact': 'hr@actionsystems.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.rmpos.com',
    'jobs_page_url': 'http://www.rmpos.com/careers.html',

    'empcnt': [51,200]
}

class RmPosJobScraper(JobScraper):
    def __init__(self):
        super(RmPosJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        
        s = soupify(self.br.response().read())
        d = s.find(text=re.compile(r'Current Openings at ASI:'))
        r = re.compile(r'^careers_')
        td = d.parent.parent.parent

        for a in td.findAll('a', href=r):
            if a.strong is not None:
                title = a.strong.text
            else:
                title = a.text

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
            td = s.html.h1.parent

            job.desc = get_all_text(td)
            job.save()

def get_scraper():
    return RmPosJobScraper()

