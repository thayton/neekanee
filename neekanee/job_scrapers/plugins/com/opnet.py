import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'OPNET',
    'hq': 'Bethesda, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.opnet.com',
    'jobs_page_url': 'https://enterprise1.opnet.com/recruiting/positions/list_jobs',

    'empcnt': [501,1000]
}

class OpnetJobScraper(JobScraper):
    def __init__(self):
        super(OpnetJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())

        na = s.find(text='North America')
        continent = na.parent.nextSibling.nextSibling               

        for division in continent.findAll('div'):
            for span in division.findAll('span'):
                ns = span.nextSibling
                while ns is not None and getattr(ns, 'name', None) != 'span':
                    ns = ns.nextSibling
                    if getattr(ns, 'name', None) == 'a':
                        l = self.parse_location(span['id'])
                        if l is None:
                            continue

                        job = Job(company=self.company)
                        job.title = ns.text
                        job.url = urlparse.urljoin(url, ns['href'])
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
            td = s.find('td', id='pagecell')

            job.desc = get_all_text(td)
            job.save()

def get_scraper():
    return OpnetJobScraper()
