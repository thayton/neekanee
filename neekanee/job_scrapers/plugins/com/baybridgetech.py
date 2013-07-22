import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bay Bridge Technologies',
    'hq': 'Annapolis, MD',

    'contact': 'recruiting@baybridgetech.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://baybridgetech.com',
    'jobs_page_url': 'http://baybridgetech.com/learn/careers/',

    'empcnt': [11,50]
}

class BayBridgeTechJobScraper(JobScraper):
    def __init__(self):
        super(BayBridgeTechJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find(text='Current Openings at Bay Bridge:')
        x = t.parent

        for p in x.findNextSiblings('p'):
            if p.a is None or \
                    re.search(r'^http://', p.a['href']) is None:
                continue

            job = Job(company=self.company)
            job.title = p.a.text
            job.url = p.a['href']
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
            d = s.html.find('div', attrs={'class': 'entry'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BayBridgeTechJobScraper()
