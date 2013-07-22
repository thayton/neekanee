import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BID2WIN',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.bid2win.com',
    'jobs_page_url': 'http://www.b2wsoftware.com/company/careers.aspx',

    'empcnt': [51,200]
}

class Bid2WinJobScraper(JobScraper):
    def __init__(self):
        super(Bid2WinJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h1' and x.text == 'B2W Careers'
        h = s.find(f)
        u = h.findNext('ul')

        for a in u.findAll('a'):
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
            x = {'class': 'title'}
            p = s.find('p', attrs=x)
            d = p.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return Bid2WinJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
