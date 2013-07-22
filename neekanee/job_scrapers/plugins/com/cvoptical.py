import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'ClearVision Optical',
    'hq': 'Hauppauge, NY',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.cvoptical.com',
    'jobs_page_url': 'http://www.cvoptical.com/AboutUs/WorkHere.htm',

    'empcnt': [51,200]
}

class CvOpticalJobScraper(JobScraper):
    def __init__(self):
        super(CvOpticalJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^WorkHere/\S+\.htm$')
        x = {'href': r, 'onclick': True, 'target': 'jobs'}

        for a in s.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.findNext(text=True)
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
            t = s.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CvOpticalJobScraper()
