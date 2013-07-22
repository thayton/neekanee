import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bol.com',
    'hq': 'Utrecht, Netherlands',

    'home_page_url': 'http://www.bol.com',
    'jobs_page_url': 'http://banen.bol.com/vacatures/',

    'empcnt': [201,500]
}

class BolJobScraper(JobScraper):
    def __init__(self):
        super(BolJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='content')
            x = {'class': 'entry'}

            for v in d.findAll('div', attrs=x):
                job = Job(company=self.company)
                job.title = v.h2.text
                job.url = urlparse.urljoin(self.br.geturl(), v.h2.a['href'])
                job.location = self.company.location
                jobs.append(job)

            n = s.find('div', id='next')
            if n.a is None:
                break

            u = urlparse.urljoin(self.br.geturl(), n.a['href'])
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BolJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
