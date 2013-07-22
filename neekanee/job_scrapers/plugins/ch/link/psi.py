import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Paul Scherrer Institute',
    'hq': 'Villigen, Switzerland',

    'home_page_url': 'http://www.psi.ch',
    'jobs_page_url': 'http://www.psi.ch/pa/offenestellen/',

    'empcnt': [1001,5000]
}

class PsiJobScraper(JobScraper):
    def __init__(self):
        super(PsiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='jobs')
        r = re.compile(r'/pa/offenestellen/[0-9-]+$')
        
        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)
            break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')
            x = {'class': 'maincontent'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PsiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
