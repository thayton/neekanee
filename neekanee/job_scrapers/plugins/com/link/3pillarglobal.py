import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '3Pillar Global',
    'hq': 'Fairfax, VA',

    'home_page_url': 'http://www.3pillarglobal.com',
    'jobs_page_url': 'http://www.3pillarglobal.com/who-we-are/careers',

    'empcnt': [501,1000]
}

class ThreePillarJobScraper(JobScraper):
    def __init__(self):
        super(ThreePillarJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='open-positions')
        r = re.compile(r'/jobs/details\.php\?jid=[a-z0-9]+$')
        x = re.compile(r'(tab-\d+-content)')

        for a in d.findAll('a', href=r):
            v = a.findParent('div', attrs={'class': x})
            m = re.search(x, v['class'])

            p = d.find('li', attrs={'rel': m.group(1)})
            l = self.parse_location(p.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            t = s.find('table', id='maintable')
            
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ThreePillarJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
