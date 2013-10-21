import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ooyala',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.ooyala.com',
    'jobs_page_url': 'http://www.ooyala.com/about/careers',

    'empcnt': [201,500]
}

class OoyalaJobScraper(JobScraper):
    def __init__(self):
        super(OoyalaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'careers'}
        d = s.find('div', attrs=x)
        x = {'class': 'position', 'location': True}
        
        for v in d.findAll('div', attrs=x):
            l = self.parse_location(v['location'])
            if not l:
                continue

            job = Job(company=self.company)
            job.title = v.a.text
            job.url = urlparse.urljoin(self.br.geturl(), v.a['href'])
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
            h = s.find('h1', id='page-title')
            d = h.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OoyalaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
