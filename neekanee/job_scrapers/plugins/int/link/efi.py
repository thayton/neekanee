import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'European Forest Institute',
    'hq': 'Joensuu, Findland',

    'home_page_url': 'http://www.efi.int',
    'jobs_page_url': 'http://www.efi.int/portal/careers/open_jobs/',

    'empcnt': [51,200]
}

class WhoJobScraper(JobScraper):
    def __init__(self):
        super(WhoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'\?bid=\d+$')

        for a in s.findAll('a', href=r):
            t = a.span.text.split(',', 1)
            if len(t) < 2:
                continue

            l = re.sub(r'\(.*\)', '', t[1])
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = t[0]
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
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WhoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
