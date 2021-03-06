import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Thompson Bros Construction',
    'hq': 'Spruce Grove, Canada',

    'home_page_url': 'http://www.thompsonbros.com',
    'jobs_page_url': 'http://www.thompsonbros.com/index.php/site/careers/',

    'empcnt': [501,1000]
}

class ThompsonBrosJobScraper(JobScraper):
    def __init__(self):
        super(ThompsonBrosJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobTitle'}
        y = {'class': 'jobLocation'}
        
        for p in s.findAll('p', attrs=x):
            if not p.a:
                continue

            d = p.findParent('div')
            l = d.find('p', attrs=y)
            l = self.parse_location(l.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = p.a.text
            job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
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
            d = s.find('div', id='jobPostDetails')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ThompsonBrosJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
