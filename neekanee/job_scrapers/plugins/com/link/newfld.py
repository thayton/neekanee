import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Newfield Exploration',
    'hq': 'The Woodlands, TX',

    'home_page_url': 'http://www.newfld.com',
    'jobs_page_url': 'http://newfield-career-opportunities.ttcportals.com/jobs/',

    'empcnt': [1001,5000]
}

class NewfldJobScraper(JobScraper):
    def __init__(self):
        super(NewfldJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'entry item'}
        y = {'class': 'meta_location'}
        v = s.find('div', id='jobs')

        for d in v.findAll('div', attrs=x):
            l = d.find('li', attrs=y)
            l = self.parse_location(l.a.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = d.h3.a.text
            job.url = urlparse.urljoin(self.br.geturl(), d.h3.a['href'])
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
            d = s.find('div', id='job')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NewfldJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
