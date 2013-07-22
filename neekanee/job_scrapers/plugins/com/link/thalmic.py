import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Thalmic Labs',
    'hq': 'Kitchener, Canada',

    'home_page_url': 'http://www.thalmic.com',
    'jobs_page_url': 'https://www.thalmic.com/careers/',

    'empcnt': [11,50]
}

class ThalmicJobScraper(JobScraper):
    def __init__(self):
        super(ThalmicJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='posts')
        r = re.compile(r'^/careers/[^/]+/$')
        f = lambda x: x.name == 'a' and x.get('href', None) and re.search(r, x['href']) and x.text == 'Learn More'

        for a in s.findAll(f):
            p = a.findParent('div')
            l = self.parse_location(p.h5.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = p.h4.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            d = s.find('div', id='wrap')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ThalmicJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
