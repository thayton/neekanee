import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Newmarket International',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://newmarketinc.com',
    'jobs_page_url': 'http://newmarketinc.com/careers/',

    'empcnt': [201,500]
}

class NewmarketIncJobScraper(JobScraper):
    def __init__(self):
        super(NewmarketIncJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/careers/[^/]+$')
        d = s.find('div', id='copyBlock')

        for a in d.findAll('a', href=r):
            if len(a.text) == 0:
                continue

            l = a.text.rsplit('-', 1)
            l = self.parse_location(l[1])
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
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
            d = s.find('div', id='MainLftTwoColumnWhite')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NewmarketIncJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
