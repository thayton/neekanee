import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Multiplica',
    'hq': 'Miami, FL',

    'home_page_url': 'http://www.multiplica.com',
    'jobs_page_url': 'http://ww2.multiplica.com/en/contact-us/',

    'empcnt': [51,200]
}

class MultiplicaJobScraper(JobScraper):
    def __init__(self):
        super(MultiplicaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'columns six first'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/cast/[^/]+/$')
        x = {'class': 'adv'}

        for p in d.findAll('p', attrs=x):
            h6 = p.findPrevious('h6')
            job = Job(company=self.company)
            job.title = h6.text
            job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
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
            r = re.compile(r'talento_detail')
            x = {'class': r}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MultiplicaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()