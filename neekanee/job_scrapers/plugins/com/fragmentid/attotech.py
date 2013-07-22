import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ATTO Technology',
    'hq': 'Amherst, NY',

    'home_page_url': 'http://www.attotech.com',
    'jobs_page_url': 'http://www.attotech.com/corporate/careers/',

    'empcnt': [51,200]
}

class AttoTechJobScraper(JobScraper):
    def __init__(self):
        super(AttoTechJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        u = s.find('ul', attrs={'class': 'careerList noBullets'})
        r = re.compile(r'^/corporate/careers/\d+/')

        for h3 in u.findAll('h3'):
            a = h3.find('a', href=r)
            if not a:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
        
            x = a.findParent('li')
            p = x.p.contents[-1]

            z = re.compile(r'\(corporate headquarters\)', re.I)
            l = re.sub(z, '', p)
            l = re.sub(r' or .*', '', l)
            l = self.parse_location(l)

            if not l:
                continue
                   
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
            x = {'class': 'grid_12'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AttoTechJobScraper()
