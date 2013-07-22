import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'United Safety',
    'hq': 'Airdrie, Canada',

    'home_page_url': 'http://www.unitedsafety.net',
    'jobs_page_url': 'http://careers.unitedsafety.net',

    'empcnt': [501,1000]
}

class UnitedSafetyJobScraper(JobScraper):
    def __init__(self):
        super(UnitedSafetyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'\.html#more$')
        x = {'href': r, 'title': True}
        y = {'class': 'post-outer'}

        for a in s.findAll('a', attrs=x):
            d = a.findParent('div', attrs=y)
            job = Job(company=self.company)
            job.title = d.h3.text
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
            d = s.find('div', id='main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return UnitedSafetyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
