import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Acid21',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.acid21.com',
    'jobs_page_url': 'http://www.acid21.com/en/Jobs/',

    'empcnt': [11,50]
}

class Acid21JobScraper(JobScraper):
    def __init__(self):
        super(Acid21JobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='innerContentWrapper')
        f = lambda x: x.name == 'h1' and x.text == 'Jobs'
        h = s.find(f)
        u = h.findNext('ul')
        x = {'target': '_self'}

        for a in u.findAll('a', attrs=x):
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
            d = s.find('div', id='innerContentWrapper')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return Acid21JobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
