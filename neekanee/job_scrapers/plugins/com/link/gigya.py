import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Gigya',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.gigya.com',
    'jobs_page_url': 'http://www.gigya.com/careers/',

    'empcnt': [51,200]
}

class GigyaJobScraper(JobScraper):
    def __init__(self):
        super(GigyaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-title'}

        for d in s.findAll('div', attrs=x):
            l = self.parse_location(d.p.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = d.a.text
            job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
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
            d = s.find('div', id='content')
            x = {'class': 'detail-header'}
            d = d.find('div', attrs=x)
            d = d.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GigyaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
