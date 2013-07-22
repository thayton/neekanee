import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Thermonuclear Experimental Reactor - ITER',
    'hq': 'St. Paul-lez-Durance France',

    'home_page_url': 'http://www.iter.org',
    'jobs_page_url': 'http://www.iter.org/jobs',

    'empcnt': [51,200]
}

class IterJobScraper(JobScraper):
    def __init__(self):
        super(IterJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job_tble'}

        for td in s.findAll('td', attrs=x):
            tr = td.findParent('tr')
            if td != tr.findAll('td')[0]:
                continue

            if td.a is None:
                continue

            job = Job(company=self.company)
            job.title = td.a.text
            job.url = urlparse.urljoin(self.br.geturl(), td.a['href'])
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
            d = s.find('div', id='subform')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IterJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
