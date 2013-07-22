import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Chartbeat',
    'hq': 'New York, NY',

    'home_page_url': 'http://chartbeat.com',
    'jobs_page_url': 'http://chartbeat.com/jobs/',

    'empcnt': [1,10]
}

class ChartbeatJobScraper(JobScraper):
    def __init__(self):
        super(ChartbeatJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs-main'}
        ul = s.find('ul', attrs=x)
        x = {'class': 'job-posting-item'}

        for li in ul.findAll('li', attrs=x):
            job = Job(company=self.company)
            job.title = li.a.text
            job.url = urlparse.urljoin(self.br.geturl(), li.a['href'])
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
            x = {'class': 'jobs-main'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ChartbeatJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
