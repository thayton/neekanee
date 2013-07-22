import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cerona Networks',
    'hq': 'Frederick, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.cerona.com',
    'jobs_page_url': 'http://www.cerona.com/careers.html',

    'empcnt': [11,50]
}

class CeronaJobScraper(JobScraper):
    def __init__(self):
        super(CeronaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        h = s.html.h2

        for a in h.findAll('a'):
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
            t = s.body.find(text=re.compile(r'CAREERS WITH CERONA'))
            t = t.parent.parent.parent

            l = t.find(text=re.compile(r'LOCATION:'))
            l = l.parent.findNext('h5')
            l = self.parse_location(l.text)
            
            if l:
                job.location = l

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CeronaJobScraper()
