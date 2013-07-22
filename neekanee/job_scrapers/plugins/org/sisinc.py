import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Spatial Integrated Systems, Inc., (SIS)',
    'hq': 'Calverton, MD',

    'home_page_url': 'http://www.sisinc.org',
    'jobs_page_url': 'http://www.sisinc.org/careers.html',

    'empcnt': [11,50]
}

class SisJobScraper(JobScraper):
    def __init__(self):
        super(SisJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^job\d+\.html')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.location = self.company.location

            if a.text.find('(') != -1:
                m = re.search(r'\((.*)\)', a.text)
                l = self.parse_location(m.group(1))

                if l:
                    job.location = l

            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        r = re.compile(r'^job\d+\.html')

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = s.find('a', href=r)
            t = a.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return SisJobScraper()
