import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bryn Mawr College',
    'hq': 'Bryn Mawr, PA',

    'home_page_url': 'http://www.brynmawr.edu',
    'jobs_page_url': 'http://www.brynmawr.edu/humanresources/Recruit/employment_opportunities.shtml',

    'empcnt': [201,500]
}

class BrynMawrJobScraper(JobScraper):
    def __init__(self):
        super(BrynMawrJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='siteContentContainer')
        f = lambda x: x.name == 'h2' and x.text == 'Employment Opportunities'
        h = d.find(f)
        d = h.findParent('div')
        f = lambda x: x.name == 'a' and x.parent.name == 'p'

        for a in d.findAll(f):
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
            d = s.find('div', id='siteContentContainer')
            x = {'class': 'two-thirds'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BrynMawrJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
