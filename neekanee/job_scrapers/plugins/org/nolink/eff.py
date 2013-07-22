import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Electronic Frontier Foundation (EFF)',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.eff.org',
    'jobs_page_url': 'https://www.eff.org/about/opportunities/jobs',

    'empcnt': [11,50]
}

class EffJobScraper(JobScraper):
    def __init__(self):
        super(EffJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'panel-pane pane-views pane-job-openings'}
        r = re.compile(r'^/opportunities/jobs/[a-z-]+$')
        d = s.find('div', attrs=x)
        d.extract()

        for a in d.findAll('a', href=r):
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
            x = {'class': 'pane-title'}
            h = s.find('h2', attrs=x)
            d = h.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EffJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
