import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'On Deck Capital',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.ondeckcapital.com',
    'jobs_page_url': 'http://www.ondeckcapital.com/careers',

    'empcnt': [51,200]
}

class OnDeckCapitalJobScraper(JobScraper):
    def __init__(self):
        super(OnDeckCapitalJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/careers/\d+/\d+-\S+$')

        for a in s.findAll('a', href=r):
            p = a.findPrevious('p')
            l = getattr(p.contents[2], 'text', p.contents[2])
            m = re.search(r'Location: (.*)', l)
            if not m:
                continue

            l = self.parse_location(m.group(1))
            if not l:
                continue

            job = Job(company=self.company)
            job.title = p.strong.text
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
            d = s.find('div', id='page')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OnDeckCapitalJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
