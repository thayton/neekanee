import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Telecommunication Union',
    'hq': 'Geneva, Switzerland',

    'home_page_url': 'http://www.itu.int',
    'jobs_page_url': 'https://erecruit.itu.int/public/index.asp?lng=en&vaclng=en',

    'empcnt': [501,1000]
}

class WhoJobScraper(JobScraper):
    def __init__(self):
        super(WhoJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'hrd-cl-vac-view\.asp\?jobinfo_uid_c=\d+.*lng=\s*en$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), ''.join(a['href'].split()))
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find(text=re.compile(r'^Duty Station:'))

            if not t:
                continue

            t = t.findParent('td')
            l = self.parse_location(t.contents[-1])

            if not l:
                continue

            t = t.findParent('table')
            t = t.findParent('table')

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return WhoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
