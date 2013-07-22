import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'SusQTech',
    'hq': 'Winchester, VA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.susqtech.com',
    'jobs_page_url': 'http://www.susqtech.com/about/jobs/Pages/default.aspx',

    'empcnt': [11,50]
}

class SusQTechJobScraper(JobScraper):
    def __init__(self):
        super(SusQTechJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        h = s.find(text='Open Positions').parent
        u = h.findNext('ul')

        for l in u.findAll('li'):
            job = Job(company=self.company)
            job.title = l.a.text
            job.url = urlparse.urljoin(self.br.geturl(), l.a['href'])
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
            d = s.find('div', id='sqt-page-main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SusQTechJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
