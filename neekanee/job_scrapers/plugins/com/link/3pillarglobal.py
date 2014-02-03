import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_del

from neekanee_solr.models import *

COMPANY = {
    'name': '3Pillar Global',
    'hq': 'Fairfax, VA',

    'home_page_url': 'http://www.3pillarglobal.com',
    'jobs_page_url': 'http://cats.3pillarglobal.com/jobs/',

    'empcnt': [501,1000]
}

class ThreePillarJobScraper(JobScraper):
    def __init__(self):
        super(ThreePillarJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^details\.php\?jid=')

        for a in s.findAll('a', href=r):
            p = a.findParent('li')
            l = self.parse_location(p.span.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_query_del(job.url, 'PHPSESSID')
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
            t = s.h1.findParent('table')
            t = t.findParent('table')
            
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ThreePillarJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
